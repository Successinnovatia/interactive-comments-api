from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            #verify the id auth_token gotten from the client
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            #check if the the issuer of the token is the google server
            if 'accounts.google.com' in idinfo['iss']: 
                return idinfo
        #throw an error if the the check doesnt pass
        except:
            return "The token is either invalid or has expired"