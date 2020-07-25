from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import PasswordContextMixin, FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms


def profile(request):
    return render(request, "registration/profile_layout.html")


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/profile')
def create_account_done(request):
    return render(request, "registration/create_account_done.html")


class CreateAccountView(PasswordContextMixin, FormView):
    email_template_name = 'registration/create_account_email.html'
    extra_email_context = None
    form_class = forms.CreateAccountForm
    from_email = None
    html_email_template_name = 'registration/create_account_email.html'
    subject_template_name = 'registration/create_account_subject.txt'
    success_url = reverse_lazy('create_account_done')
    template_name = 'registration/create_account_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/accounts/profile'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)
