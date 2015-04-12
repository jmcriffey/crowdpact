from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from crowdpact.views import CrowdPactView


class AccountLoginView(CrowdPactView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        account = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if account:  # TODO redirect the user.
            login(request, account)

            return self.get_json_response({'message': 'Welcome to CrowdPact!'})

        return self.get_json_response({'message': 'Bad username or password.'})


class AccountSignupView(CrowdPactView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').lower()
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')

        try:
            self.validate_user(username, email, password)
        except ValidationError as err:
            return self.get_json_response({'message': str(err[0])})

        get_user_model().objects.create_user(email=email, username=username, password=password)

        account = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        login(request, account)

        # TODO: redirect the user
        return self.get_json_response({'message': 'Welcome to CrowPact!'})

    def validate_user(self, username, email, password):
        if len(password) < 7:
            raise ValidationError(message='A password is of at least 7 characters is required.')

        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError(message='That username is already taken.')

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(message='That email address is already taken.')

        validate_email(email)
