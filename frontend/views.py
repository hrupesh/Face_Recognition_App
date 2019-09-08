from __future__ import unicode_literals
from .serializers import UserSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from .serializers import LoginSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .forms import UserForm
from .models import User, Image
from rest_framework import viewsets
from .serializers import UserSerializer
import os
from .serializers import UserSerializer , checkimageserializer

# class userview(ListModelMixin , GenericAPIView):
#     print('hey')
#     serializer_class = UserSerializer
#     queryset = Users.objects.all()
#     print(queryset)
#     #return Response({"User": User})

#     def perform_create(self, serializer):
#         Users = get_object_or_404(Users, id=self.request.data.get('Users_id'))
#         return serializer.save(Users=Users)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


def register(request):
    # print(os.system(pwd))
    return render(request, 'register.html', {'msg': 'Fill the Form', 'status': 'warning'})


def upload(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            user = User(name=name, email=email)
            user.save()
            for file in request.FILES.getlist('user_img'):
                img = Image(user=user, user_img=file)
                img.save()
                user.img.add(img)
            user.save()
            return render(request, 'register.html', {'msg': 'Data Uploaded Successfully', 'status': 'success'})
        except Exception as e:
            return render(request, 'register.html', {'msg': "User already exists! Try again with different name.", 'status': 'danger'})
    return HttpResponseRedirect('/')


# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter, SearchFilter
# from django_filters import FilterSet
# from django_filters import rest_framework as filters


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "User Successfully Logged in."}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication)

    def post(self, request):
        django_logout(request)
        return Response(status=204)




class PollListView(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class imgviewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = checkimageserializer

from rest_framework import serializers
from rest_framework import views
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser , FileUploadParser

@api_view(["POST"])
def img_check(request):
    print('you entered')
    print(request)
    print(request.data)
    img = request.data
    return Response("Image uplaodes is"+str(img))
    #try:
     #   print('entry')
      #  print(request)
       # value =  json.loads(request.body)       
        #print('entry')
        #print (value)       
        #su = sum(value)
        #print(su)
        #return Response("Sum is :"+str(su))
    #except:
     #   return Response(status.HTTP_400_BAD_REQUEST)
    

    #def get(self, request):
        # Validate the incoming input (provided through query parameters)
        #serializer = IncredibleInputSerializer(data=request.query_params)
        #serializer.is_valid(raise_exception=True)

        # Get the model input
        #data = serializer.validated_data
        #model_input = data["i"]

        # Perform the complex calculations
        #complex_result = model_input + "xyz"

        # Return it in your custom format

class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename ,format=None):
        try:
            file_obj = request.data['file']
            print(file_obj)
            if(file_obj):
                return Response(status=200)
        except:
            return Response(status=400)
        return Response(status=204)
