from django.contrib.auth import authenticate
from authentication.models import User
import os
import random

from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):
    username = "".join(name.split(' ')).lower()

    if not User.objects.filter(username=username).exists():
        return username

    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    #check if user already has an email
    filtered_user_by_email = User.objects.filter(email=email)
    #check if the user already has an account in our application
    if filtered_user_by_email.exists():

        # if true check if the provider the user has signed up with before is the same provider the user is using currently 
        if provider == filtered_user_by_email[0].auth_provider:
            #if true authenticate user and return user info: social_secret is a randomsecret key used to validate the user from the backend
            registered_user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))


            return{
                'username':registered_user.username,
                'email':registered_user.email,
                'tokens':registered_user.tokens() 

            }
        #if the user is trying to sign in with provider that they didnt use before but uses the same email on different platforms the user is directed to login with their provider
        else:
            raise AuthenticationFailed(
                detail = 'please continue your login using ' + filtered_user_by_email[0].auth_provider
            )
    #create an account for the user since they dont have an account
    else:
        user = {
            'username': generate_username(name),
            'email':email,
            'password':os.environ.get('SOCIAL_SECRET')
        }
        user = User.objects.create_user(**user)

        user.is_verified = True

        user.auth_provider = provider

        user.save()

        new_user = authenticate(
            email = email, password=os.environ.get('SOCIAL_SECRET')
        )

        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens':new_user.tokens()
        }