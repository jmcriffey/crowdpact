from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.shortcuts import redirect

from crowdpact.views import CrowdPactView


class AccountLoginView(CrowdPactView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        account = authenticate(
            username=request.POST.get('username', '').lower(),
            password=request.POST.get('password')
        )

        if account:
            login(request, account)

            return self.get_json_response({'next': reverse('pact.index')})

        return self.get_json_response({'message': 'Bad username or password.'})


class AccountLogoutView(CrowdPactView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('landing.index')


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

        if account:
            login(request, account)

            return self.get_json_response({'next': reverse('pact.index')})

        return self.get_json_response({'message': 'There was an error signing up.'})

    def validate_user(self, username, email, password):
        if len(password) < 7:
            raise ValidationError(message='A password is of at least 7 characters is required.')

        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError(message='That username is already taken.')

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(message='That email address is already taken.')

        validate_email(email)
