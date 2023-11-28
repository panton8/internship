from users.authentication import JWTAuthentication


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_class = JWTAuthentication()
        auth_result = auth_class.authenticate(request)
        if auth_result:
            user, token = auth_result
            request.user = user
            request.auth = token

        response = self.get_response(request)
        return response
