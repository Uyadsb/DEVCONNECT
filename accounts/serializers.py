from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'birthdate']


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User  
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password2', 'birthdate', 'sex']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, data):
        # Vérifie que les deux mots de passe correspondent.
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"password2": "Les mots de passe ne correspondent pas."})
        return data
    
    def create(self, validated_data):
        # Crée un nouvel utilisateur avec un mot de passe hashé.
        validated_data.pop('password2')  # On supprime password2 car il n'est pas stocké en base
        user = User.objects.create_user(**validated_data)
        return user
    
    
# login serializers
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # username ou email
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')
        
        if not identifier or not password:
            raise serializers.ValidationError("Les identifiants sont requis pour se connecter.")
        
        # Pass the identifier as 'username' parameter to match what the backend expects
        user = authenticate(request=self.context.get('request'), 
                            username=identifier, password=password)
        
        if not user:
            raise serializers.ValidationError("Identifiants invalid !")
        
        data['user'] = user
        return data
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=500, )
    
    def validate(self, data):
        try:
            refresh_token = data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return serializers.ValidationError("Token invalide ou expired.")
        return data