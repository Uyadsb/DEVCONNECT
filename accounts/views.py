# from ret_framework import
from .serializers import UserSerializer, SignUpSerializer, LoginSerializer, LogoutSerializer
from rest_framework import viewsets,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.
class UserViewsets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)



# signup view
class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer  
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return User.objects.all()
        
    def get(self, request, *args, **kwargs):
        return Response({"error": "Méthode GET non autorisée"}, status=405)



# login view
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializers = LoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        
        # generate jwt token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }, status= status.HTTP_200_OK)     

      
# logout view
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]    
    
    def post(self, request):
        serializers = LogoutSerializer(data=request.data)
        if serializers.is_valid():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializers.errors, status=status.HTTP_404_BAD_REQUEST) 