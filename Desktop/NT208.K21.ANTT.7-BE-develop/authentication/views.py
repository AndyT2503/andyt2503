from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
#renders help format return json to client
from .renderers import UserJSONRenderer

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # Set serializer class
    serializer_class = RegistrationSerializer
    # Set UserJSONRenderer as renderer
    renderer_classes = [UserJSONRenderer,]

    def post(self, request):
        user = request.data.get('user', {})
        if user == {}:
            user = request.data
        #validate by RegistrationSerializer
        serializer = self.serializer_class(data=user)
        #raise_exception true to handle and return JSON format ValidationErrors to client
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        # context={"request": request} will return full url of imageField
        serializer = self.serializer_class(request.user, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        if serializer_data == {}:
            serializer_data = request.data
        # By default, serializers must be passed values for all required fields or they will raise validation errors.
        #You can use the partial argument in order to allow partial updates.

        #pass request.user object so when call serializer.save it call update func
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        #Calling .save() will either create a new instance, or update an existing instance,
        #depending on if an existing instance was passed when instantiating the serializer class
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
