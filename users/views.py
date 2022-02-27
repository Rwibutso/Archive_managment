import imp
from lib2to3.pgen2 import token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import  AuthToken
from . import serializers



@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    __,  token = AuthToken.objects.create(user)


    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
            },
        'token': token
    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
           'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
    })

    return Response({'error': 'You are not authanticated!'}, status=400)


@api_view(['POST'])
def register_api(request):
    serializer = serializers.RegisterSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    __, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
            },
        'token': token
    }) 