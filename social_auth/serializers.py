from rest_framework import serializers
from . import google, facebook
from .register import register_social_user 

import os

from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer:
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider = provider,
                user_id = user_id,
                email=email,
                name = name
            )

        except Exception as identifier:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    #set auth_token to charfield to expose the serializer to the view
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        #validate the token using the validator in google.py file
        user_data = google.Google.validate(auth_token)

        try:
            #check if the user information is gotten correctly through the id: the sub is the id in google language
            user_data['sub']
        
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        #check if the audience for the user information is our application: the client id is the one gotten from google for our app, it will also be sent by the client to google and then to the server
        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')


        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider = provider, user_id=user_id, email=email, name=name
        )

