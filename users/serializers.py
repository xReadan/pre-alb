from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers



class RegisterUserSerializer(serializers.ModelSerializer):
    # Ensure that an email is already used
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    # By implementing "write_only=True", the password will not be sent back to the user
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'username': {'required': True}
        }
    
    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username', 'id', 'avatar', 'type')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }