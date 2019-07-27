from .models import User,Image
from rest_framework import viewsets , permissions
from .serializers import UserSerializer,ImageSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    
    serializer_class = UserSerializer
    queryset = User.objects.all()



class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()