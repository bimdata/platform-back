from django.views.generic import TemplateView, View, RedirectView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.conf import settings
from django.urls import reverse


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class FrontCallbackView(TemplateView):
    template_name = "front_callback.html"


class BackCallbackView(View):
    def get(self, request):
        user = authenticate(request, nonce=request.GET.get("nonce"))
        if user:
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")


class SignUpView(RedirectView):
    def get_redirect_url(self):
        return "{url}?next={next}".format(
            url=settings.OIDC_OP_SIGNUP_URL,
            next=self.request.build_absolute_uri(reverse("oidc_authentication_init")),
        )
