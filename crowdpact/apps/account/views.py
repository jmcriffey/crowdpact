from django.views.generic import TemplateView


class AccountSignupView(TemplateView):
    app = 'AccountSignupApp'
    template_name = 'index.html'
    title = 'Signup'

    def get_context_data(self):
        context = super(AccountSignupView, self).get_context_data()

        context['title'] = self.title
        context['app'] = self.app

        return context
