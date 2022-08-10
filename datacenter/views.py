import email
import token
from django.http import JsonResponse
from tokenize import Token
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import DatacenterSerializer, RequestSerializer
from .models import AgencyRegister
import jwt, datetime

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
            return JsonResponse(data, safe=False)

        if not user.check_password(password):
            data = {
                'statusCode' : 1000,
                'errorMsg' : 'PASSWORD_INVALID'
            }
            return JsonResponse(data, safe=False)
            

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

