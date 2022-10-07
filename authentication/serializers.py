from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    password = serializers.CharField(max_length =128, min_length =6, write_only = True)

    """
    write_only = True,  is to ensure that the field may be used when updating or creating an instance, but is not included when serializing or displaying the representation
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        #the fields that are to be shown to the user when registering

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length =128, min_length =6, write_only = True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

        read_only_fields = ['token']