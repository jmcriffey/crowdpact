from django.contrib.auth import authenticate

from crowdpact.views import CrowdPactView


class AccountLoginView(CrowdPactView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        account = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if account:
            return self.get_json_response({'message': 'You logged in.'})
        else:
            return self.get_json_response({'message': 'Bad username or password.'})
