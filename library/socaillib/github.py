from django.conf import settings
import urllib.request as requests
import json


class Github:
    """
    Github class to fetch the user info and return it
    """

    @staticmethod
    def validate(access_token):
        """
        validate method Queries the github url to fetch the user info
        """
        try:
            headers = {
                "Authorization": f"token {access_token}",
                "content-type": "application/json",
                "Access-Control-Expose-Headers": "ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval",
            }
            user_info_url = "https://api.github.com/user/emails"
            req = requests.Request(user_info_url, headers=headers)
            response = requests.urlopen(req)
            response = response.read()
            data = response.decode("utf-8")
            user_info = json.loads(data)
            return user_info[0]
        except:
            return "The token is either invalid or has expired"
