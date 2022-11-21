from django.http import JsonResponse,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import DatacenterSerializer, RequestSerializer,FileSerializer,MetaDataSerializer
from .models import AgencyRegister, Province,DataSetGroup,MetadataGroup,Metadata,File,MetaDataMapField
import jwt, datetime
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status,viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from wsgiref.util import FileWrapper
import os
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords

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
        return Response(data={"statusCode":0,"data":{"result" : serializer.data}} )


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
            'userId': user.userId,
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

        user = AgencyRegister.objects.filter(userId=payload['userId']).first()
        serializer = DatacenterSerializer(user)

        return Response(data={"statusCode":0, "data" : serializer.data})


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'statusCode' : 0,
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
        dataMapName = request.POST.getlist('dataMapId')
        dataMapUser = request.POST.getlist('dataMapUser')
        descriptionDataMap = request.POST.getlist('descriptionDataMap')
        province = Province.objects.filter(name_th=request.POST['provinceId']).first()
        word = str(request.POST['description']) + province.name_th
        list_word = word_tokenize(str(word))
        stopwords = list(thai_stopwords())
        list_word_not_stopwords = [i for i in list_word if i not in stopwords and i!=" "]
        keyWord = ','.join(str(i) for i in list_word_not_stopwords)
        dataSet = DataSetGroup.objects.filter(dataSetGroupName=request.POST['dataSetGroupId']).first()
        metadata = Metadata.objects.create(
            dataSetGroupId=dataSet.dataSetGroupId,
            fileName=request.POST['fileName'],
            provinceId=province.id,
            dataName=request.POST['dataName'],
            description=request.POST['description'],
            userId=request.POST['userId'],
            stopWord=keyWord
            )
        
        x = len(dataMapName)

        for i in range(x):
            m = MetadataGroup.objects.filter(metadataGroupName=dataMapName[i]).first()
            MetaDataMapField.objects.create(
                metadataId=metadata.metadataId,
                metadataGroupId=m.metadataGroupId,
                fieldNameUser=dataMapUser[i],
                discription=descriptionDataMap[i]
            )
            
        for file in files:
            File.objects.create( metadata=metadata ,file=file, fileName=request.POST['fileName'])
        return Response(data= {"statusCode" : 0},status=status.HTTP_201_CREATED)


class UploadNewFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        files = request.FILES.getlist('files', None)
        metadataId = request.data['metadataId']
        metaData = Metadata.objects.filter(metadataId=metadataId).first()

        for file in files:
            File.objects.create( metadata=metaData ,file=file, fileName=request.data['fileName'])
        return Response(data={"statusCode":0},status=status.HTTP_201_CREATED)

class DeleteFileView(APIView):
    def post(self, request):
        File.objects.filter(id=request.data['id']).delete()
        path = "./media/" + request.data['file']
        if os.path.exists(path):
            os.remove(path)
        return Response(data={"statusCode": 0},status=status.HTTP_200_OK)

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
        return Response(data={"statusCode":0},status=status.HTTP_200_OK)
        


class UpdataMetaDataView(APIView):
    def post(self, request):
        payload = json.loads(request.body)
        dataMapId = payload['dataMapId']
        dataMapUser = payload['dataMapUser']
        descriptionDataMap = payload['descriptionDataMap']
        print(payload['provinceId'])
        province = Province.objects.filter(name_th=payload['provinceId']).first()
        word = str(payload['description']) + province.name_th
        list_word = word_tokenize(str(word))
        stopwords = list(thai_stopwords())
        list_word_not_stopwords = [i for i in list_word if i not in stopwords and i!=" "]
        keyWord = ','.join(str(i) for i in list_word_not_stopwords)
        dataSet = DataSetGroup.objects.filter(dataSetGroupName=payload['dataSetGroupId']).first()
        MetaDataMapField.objects.filter(metadataId=payload['metadataId']).delete()
        try:
            obj = Metadata.objects.get(metadataId=payload['metadataId'])
            obj.dataSetGroupId = dataSet.dataSetGroupId
            obj.fileName = payload['fileName']
            obj.provinceId = province.id
            obj.dataName = payload['dataName']
            obj.description = payload['description']
            obj.userId = payload['userId']
            obj.stopWord = keyWord
            obj.save()
        except Metadata.DoesNotExist:
           metadata = Metadata.objects.create( 
            dataSetGroupId=dataSet.dataSetGroupId,
            fileName=payload['fileName'],
            provinceId=province.id,
            dataName=payload['dataName'],
            description=payload['description'],
            userId=payload['userId'],
            stopWord=keyWord)
        finally:
            x = len(dataMapId)
            for i in range(x):
                m = MetadataGroup.objects.filter(metadataGroupName=dataMapId[i]).first()
                MetaDataMapField.objects.create(
                    metadataId=payload['metadataId'],
                    metadataGroupId=m.metadataGroupId,
                    fieldNameUser=dataMapUser[i],
                    discription=descriptionDataMap[i]
                )
        
        return Response(data={"statusCode":0}, status=status.HTTP_200_OK)



class GetMetaDataView(APIView):
    def post(self, request):
        userId = request.data['userId']

        metaData = Metadata.objects.filter(userId=userId)
        serializer = MetaDataSerializer(metaData, many=True)
        return Response(data={"statusCode":0,"data" : {"metaData" : serializer.data}}, status=status.HTTP_200_OK)

class GetFileNameByMetaDataIdView(APIView):
    def post(self, request):
        metaDataId = request.data['metaDataId']

        files = File.objects.filter(metadata=metaDataId).values()
        fileResp = list(files)
        return Response(data={"statusCode":0,"data":{"files":fileResp}}, status=status.HTTP_200_OK)


def dropdownList(request):
    if request.method == "GET":
        province = Province.objects.all()
        dataSetGroup = DataSetGroup.objects.all()
        metadataGroup = MetadataGroup.objects.all()
        listprovicne = list(province.values())
        listdataSetGroup = list(dataSetGroup.values())
        listmetadataGroup = list(metadataGroup.values())
        return JsonResponse({"statusCode":0,"province":listprovicne, "dataSetGroup":listdataSetGroup, "metadataGroup":listmetadataGroup},safe=False)




class SearchFile(APIView):
    def post(self, request):

        class ModelSortSearch():
            def __init__(self,countMap,mateData):
                self.countMap = countMap
                self.mateData = mateData

        keyWord = request.data['keyWord']
        selectDataSetGroupId = request.data['selectDataSetGroup']
        mataDataGroupId = request.data['metaDataGroup']
        if mataDataGroupId == 0:
            resultMetaDataMapField = MetaDataMapField.objects.all()
        else:
            resultMetaDataMapField = MetaDataMapField.objects.filter(metadataGroupId=mataDataGroupId)
        mateDataIdSets = set()
        for r in resultMetaDataMapField:
            mateDataIdSets.add(r.metadataId)

        mateDataIdList = list(mateDataIdSets)
        mateDataResult = Metadata.objects.filter(metadataId__in=mateDataIdList).values()
        mateDataList = list(mateDataResult)
        metaDataResult = []
        if keyWord and keyWord != "":
            list_word = word_tokenize(str(keyWord))
            stopwords = list(thai_stopwords())
            list_word_not_stopwords = [i for i in list_word if i not in stopwords]
            print("list_word_not_stopwords : ")
            print(list_word_not_stopwords)
            allMetaData = {}
            for m in mateDataList:
                stopWordList = str(m['stopWord']).split(",")
                for i in stopWordList:
                    if i in list_word_not_stopwords:
                        if m['metadataId'] in allMetaData:
                            allMetaData[m['metadataId']].countMap += 1
                        else:
                            allMetaData[m['metadataId']] = ModelSortSearch(1,m)

            allMetaDataList = list(allMetaData.values())
            allMetaDataList.sort(key=lambda x: x.countMap, reverse=True)
        
            for i in allMetaDataList:
                metaDataResult.append(i.mateData)
        else:
            metaDataResult = mateDataList.copy()
        
        metaDataResp = []
        if selectDataSetGroupId != 0:
            for m in metaDataResult:
                if selectDataSetGroupId == m["dataSetGroupId"]:
                    metaDataResp.append(m)
        else :
            metaDataResp = metaDataResult.copy()

        dictDataSetCount = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0
        }
        for resp in metaDataResult:
            dictDataSetCount[resp["dataSetGroupId"]] += 1
        
        dictDataSet = {
            "logistic":dictDataSetCount[1], 
            "fireInOpenArea" : dictDataSetCount[2],
            "industry" : dictDataSetCount[3], 
            "construct" : dictDataSetCount[4],
            "pollution" : dictDataSetCount[5],
        }


        return Response(data={"statusCode":0,"data" : { "metaData" : metaDataResp, "dataSetCount" : dictDataSet}}, status=status.HTTP_200_OK)


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
        
       
                





