# from rest_framework.response import Response
# from rest_framework import status, exceptions
#
# from users.authentication import JWTAuthentication
#
#
# class JWTMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         auth_class = JWTAuthentication()
#
#         try:
#             user, token = auth_class.authenticate(request)
#             request.user = user
#             request.auth = token
#         except exceptions.AuthenticationFailed as auth_error:
#             request.error = str(auth_error.detail)
#
#         response = self.get_response(request)
#
#         return response

from rest_framework import exceptions

from users.authentication import JWTAuthentication


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_class = JWTAuthentication()
        auth_result = None
        try:
            auth_result = auth_class.authenticate(request)
        except exceptions.AuthenticationFailed as auth_error:
            request.error = str(auth_error.detail)

        if auth_result:
            user, token = auth_result
            request.user = user
            request.auth = token

        response = self.get_response(request)
        return response
