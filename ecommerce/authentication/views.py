from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


@api_view(['POST'])
@csrf_exempt
def login_user(request):
    username=request.POST['uname']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is None:
        return JsonResponse({'mssg':'Incorrct Credentials','status':0},status=400)
    else:
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return JsonResponse(
            data={
                'access':str(access)
            },
            status=200
        )


@api_view(['POST'])
@csrf_exempt
def register_user(request):
    username=request.POST['uname']
    password1=request.POST['password1']
    password2=request.POST['password2']

    if password1==password2: #both passwords match
        name=request.POST['name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        try:
            new_user=User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            new_user.save()
            # creation of access token
            refresh=RefreshToken.for_user(new_user)
            access=refresh.access_token

            profile=Profile()
            profile.user=new_user
            profile.name=name
            profile.mobile=mobile
            return JsonResponse(
                {
                    'mssg':"Profile created Successfully...",
                    'status':True,
                    'access_token':str(access)
                },
                status=201
            )
        except:
            return JsonResponse(
                {
                    'mssg':f"Try a different username... '{username}' is already taken ",
                    'status':False
                },
                status=400
            )
    else:
        return JsonResponse(
            data={
                'mssg':"Passwords Dont Match ... Try Again",
                'status':False
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
            )