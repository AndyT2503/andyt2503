from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Image
from django.core.exceptions import ObjectDoesNotExist
import pdb;
#create Serializer type model serializer
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=64,
        min_length=8,
        write_only=True
    )

    avatar = serializers.ImageField(source='image.file', required=False)

    #setToken to be readonly
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        #set field that can include in req.
        fields = ['email', 'name', 'avatar', 'password', 'token',]

    def create(self, validated_data):
        #**mean arbitrary number of keyword arguments as input.
        return User.objects.create_user(**validated_data)


#create Serializer default
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        #custom validate function
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'Mật khẩu hoặc email không đúng.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'name': user.name,
            'token': user.token,
        }

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    #source='image.file' mean field of user.image.file
    #when req have avatar field,set image.file in validated_data = avatar.file
    avatar = serializers.ImageField(source='image.file', required=False)
    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'token', 'avatar')

        #set token to be read only
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        #remove password from validated_data bcz default django provide func to handle update (hash..)
        password = validated_data.pop('password', None)
        #update user with fields in validated_data
        for (key, value) in validated_data.items():
            #validated_data.items() will return user model's field name, not req'field
            if key == 'image':
                try:
                    image = Image.objects.get(user=instance)
                except Image.DoesNotExist:
                    image = Image(user=instance)
                image.file = validated_data.get('image')['file']
                image.save()
            else:
                setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)
        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance