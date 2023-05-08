from google.auth.transport import requests
from google.oauth2 import id_token
import time

class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            for x in range(0,2):
                print(f"attempt to validte {x}")
                time.sleep(2)
                idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
                if 'accounts.google.com' in idinfo['iss']:
                    return idinfo
            return "The token is either invalid or has expired"