from django.shortcuts import render
from authentication.serializers import LoginSerializer, RegisterSerializer
from rest_framework.generics import GenericAPIView
# from rest_framework.views import APIView
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate


# Create your views here

#Endpoint to get current user
class AuthUserAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = RegisterSerializer
    
    def get(self, request):
        user = request.user

        serializer = RegisterSerializer(user)
        return response.Response({'user':serializer.data})


        

class RegisterAPIView(GenericAPIView):
    #authentication class is set to allow anyone visit the register and login view
    authentication_classes = []

    serializer_class = RegisterSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)


        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response({'message':'invalid credentials, try again'}, status=status.HTTP_401_UNAUTHORIZED)



# class LogoutAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.token.delete()
#         return response.Response({'message':'User Logged out successfully'}, status=status.HTTP_200_OK)