import facebook


class Facebook:
    """
    facebook class to fetch user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries from the facebook GraphAPI to fetch the user info
        """

        try:
            graph = facebook.GraphAPI(access_token = auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expired."
        