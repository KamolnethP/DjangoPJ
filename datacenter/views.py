from django.http import JsonResponse,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import DatacenterSerializer, RequestSerializer,FileSerializer,MetaDataSerializer
from .models import AgencyRegister, Province,DataSetGroup,MetadataGroup,Metadata,File
import jwt, datetime
from rest_framework.parsers import MultiPartParser, FormParser
from .document.document import MetadataDocument
from rest_framework import status,viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from wsgiref.util import FileWrapper
import os


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
        metadata = Metadata.objects.create( 
            metadataGroupId=request.POST['metadataGroupId'],
            dataSetGroupId=request.POST['dataSetGroupId'],
            fileName=request.POST['fileName'],
            provinceId=request.POST['provinceId'],
            dataName=request.POST['dataName'],
            description=request.POST['description'],
            agencyId=request.POST['agencyId'])
        for file in files:
            File.objects.create( metadata=metadata ,file=file, fileName=request.POST['fileName'])
        return Response(status=status.HTTP_201_CREATED)


class UploadNewFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        files = request.FILES.getlist('files', None)
        metadataId = request.data['metadataId']
        metaData = Metadata.objects.filter(metadataId=metadataId).first()

        for file in files:
            File.objects.create( metadata=metaData ,file=file, fileName=request.data['fileName'])
        return Response(status=status.HTTP_201_CREATED)

class DeleteFileView(APIView):
    def post(self, request):
        File.objects.filter(id=request.data['id']).delete()
        path = "./media/" + request.data['file']
        if os.path.exists(path):
            os.remove(path)
        return Response(status=status.HTTP_200_OK)

class DeleteMetaData(APIView):
    def post(self,request):
        metaDataId = request.data['metadataId']
        Metadata.objects.filter(metadataId=metaDataId).delete()
        obj = File.objects.filter(metadata_id=metaDataId).all()
        listFileName = []
        for o in obj:
            listFileName.append("./media/" +o.file)

        File.objects.filter(metadata_id=metaDataId).delete()
        for fileName in listFileName:
            if os.path.exists(fileName):
                os.remove(fileName)
        return Response(status=status.HTTP_200_OK)


        


class UpdataMetaDataView(APIView):
    def post(self, request):
        try:
            obj = Metadata.objects.get(metadataId=request.data['metadataId'])
            obj.metadataGroupId = request.data['metadataGroupId']
            obj.dataSetGroupId = request.data['dataSetGroupId']
            obj.fileName = request.data['fileName']
            obj.provinceId = request.data['provinceId']
            obj.dataName = request.data['dataName']
            obj.description = request.data['description']
            obj.agencyId = request.data['agencyId']
            obj.save()
        except Metadata.DoesNotExist:
           metadata = Metadata.objects.create( 
            metadataGroupId=request.POST['metadataGroupId'],
            dataSetGroupId=request.POST['dataSetGroupId'],
            fileName=request.POST['fileName'],
            provinceId=request.POST['provinceId'],
            dataName=request.POST['dataName'],
            description=request.POST['description'],
            agencyId=request.POST['agencyId'])
        
        return Response(data={"statusCode":"0000", "Msg":"แก้ไขแล้วนะจ้ะ"}, status=status.HTTP_200_OK)



class GetMetaDataView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = checktoken(token)
        agencyId = request.data['agencyId']

        metaData = Metadata.objects.filter(agencyId=agencyId)
        serializer = MetaDataSerializer(metaData, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class GetFileNameByMetaDataIdView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = checktoken(token)
        metaDataId = request.data['metaDataId']

        files = File.objects.filter(metadata=metaDataId).values()
        fileResp = list(files)
        return Response(data={"files":fileResp}, status=status.HTTP_200_OK)


def dropdownList(request):
    if request.method == "GET":
        province = Province.objects.all()
        dataSetGroup = DataSetGroup.objects.all()
        metadataGroup = MetadataGroup.objects.all()
        listprovicne = list(province.values())
        listdataSetGroup = list(dataSetGroup.values())
        listmetadataGroup = list(metadataGroup.values())
        return JsonResponse({"province":listprovicne, "dataSetGroup":listdataSetGroup, "metadataGroup":listmetadataGroup},safe=False)


class SearchFile(APIView):
    def post(self, request):
        keyWord = request.data['keyWord']
        s = MetadataDocument.search().filter("term", fileName =keyWord)
        listIdMetadata = []
        for hit in s:
            listIdMetadata.append(int(hit.metadataId))

        metaDataList = Metadata.objects.filter(metadataId__in=listIdMetadata).values()
        metaDataResp = list(metaDataList)
        return Response(data={"result":metaDataResp}, status=status.HTTP_200_OK)

@csrf_exempt
def downloadFile(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        filePath = mydata['filePath']
        path = "./media/" + filePath
        print(path)
        FilePointer = open(path, "rb")
        response = HttpResponse(FileWrapper(FilePointer), content_type = 'whatever')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filePath
        return response
        
       
                





