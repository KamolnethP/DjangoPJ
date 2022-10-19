from django.http import JsonResponse,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import DatacenterSerializer, RequestSerializer,FileSerializer
from .models import AgencyRegister, Province,DataSetGroup,MetadataGroup,Metadata
import jwt, datetime
from rest_framework.parsers import MultiPartParser, FormParser
from .document.document import MetadataDocument
from rest_framework import status,viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from wsgiref.util import FileWrapper


def checktoken(token):

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:

        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    except jwt.ExpiredSignatureError:        
        raise AuthenticationFailed('Unauthenticated!')
    return payload


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = DatacenterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = AgencyRegister.objects.filter(email=email).first()

        if user is None:
            data = {
                'statusCode' : 1000,
                'errorMsg' : 'USER_NOT_FOUND'
            }
            return JsonResponse(data, safe=False, status=403)

        if not user.check_password(password):
            data = {
                'statusCode' : 1000,
                'errorMsg' : 'PASSWORD_INVALID'
            }
            return JsonResponse(data, safe=False, status=403)
            

        payload = {
            'userID': user.userID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
            'iat': datetime.datetime.utcnow(),
            'isAdmin': 'False'
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'statusCode' : 0,
            'data' : {
                'jwt': token
            }
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = checktoken(token)

        user = AgencyRegister.objects.filter(userID=payload['userID']).first()
        serializer = DatacenterSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class RequestView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = checktoken(token)

        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FileView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Metadata.objects.all()
    serializer_class = FileSerializer
    def create(self, request):
        files = request.FILES.getlist('files', None)
        data = {
            "metadataGroupId" : request.POST['metadataGroupId'],
            "dataSetGroupId" : request.POST.get('dataSetGroupId', None),
            "fileName" : request.POST['fileName'],
            "provinceId" : request.POST['provinceId'],
            "dataName" : request.POST['dataName'],
            "description" : request.POST['description'],
        }
        _serializer = self.serializer_class(data=data,context={'files': files, 'data': data})
        if _serializer.is_valid():
            _serializer.save()
            s = MetadataDocument.search().filter("term", description ="pm2.5")
            for hit in s :
                print(hit.fileName)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)  
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def dropdownList(request):
    if request.method == "GET":
        province = Province.objects.all()
        dataSetGroup = DataSetGroup.objects.all()
        metadataGroup = MetadataGroup.objects.all()
        listprovicne = list(province.values())
        listdataSetGroup = list(dataSetGroup.values())
        listmetadataGroup = list(metadataGroup.values())
        return JsonResponse({"province":listprovicne, "dataSetGroup":listdataSetGroup, "metadataGroup":listmetadataGroup},safe=False)

@csrf_exempt
def searchFile(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        keyWord = mydata['keyWord']
        filterPovince = mydata['filterPovince']
        filterMetadataGroup = mydata['filterMetadataGroup']
        filterDataSetGroup = mydata['filterDataSetGroup']
        s = MetadataDocument.search().filter("term", fileName =keyWord)
        listIdMetadata = []
        for hit in s:
            listIdMetadata.append(int(hit.D_MetadataID))
        sql = "SELECT * FROM datacenter_metadata WHERE 1"
        if len(listIdMetadata) > 0 :
            sql += " AND D_MetadataID in %s"
        if filterPovince:
            sql += " AND D_PROVINCE = " + str(filterPovince)
        if filterMetadataGroup:
            sql += " AND D_TypeID = " + str(filterMetadataGroup)
        if filterDataSetGroup:
            sql += " AND D_GroupID = " + str(filterDataSetGroup)

        dataResp = []
        if len(listIdMetadata) > 0 :
            listData = Metadata.objects.raw(sql, params=[listIdMetadata])
            dataResp = listData
        else:
            listData = Metadata.objects.raw(sql)
            dataResp = listData

        context = serializers.serialize('json',dataResp)
        dataDict = json.loads(context)
        return JsonResponse({"data": dataDict},safe=False)

@csrf_exempt
def downloadFile(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        filename = mydata['filename']
        filePath = mydata['filePath']
        FilePointer = open(filePath, "rb")
        response = HttpResponse(FileWrapper(FilePointer), content_type = 'whatever')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response
        
       
                





