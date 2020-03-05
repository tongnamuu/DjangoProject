from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms, models
import os
import requests

# Create your views here.

# 로그인시 csrf 에러가 뜰 수 있다 Cross Site Request Forgery 사이트간 요청 위조
# 웹사이트가 널 로그인 시켜줄 때 웹사이트는 쿠키를 준다.
# 브라우저가 백엔드로 쿠키를 보내는 방식은 도메인에 의해 이루어진다
# 페이스북이 너에게 쿠키를 주고나면 다음부턴 페이스북에 접속할 때마다 자동적으로 쿠키를 페이스북으로 보낸다
# 페이스북이 아닌 다른 웹사이트에 접속했을 때 문제가 된다
# 그 웹사이트가 이상한 버튼을 가지고 있다
# 그 버튼을 누르면 페이스북에 요청을 보낸다
# 요청은 너의 브라우저에서 일어났기 때문에 브라우저는 쿠키를 보낼 것이다
# 너가 다른 웹사이트에서 페이스북으로 form을 보내는 것
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "tongnamuu@naver.com"})
#         return render(request, "users/login.html", {"form": form,})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 print("######login#########")
#                 return redirect(reverse("core:home"))
#             else:
#                 print("Error")
#         return render(request, "users/login.html", {"form": form,})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "tongnamuu",
        "last_name": "Rorschach",
        "email": "tongnamuu@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            user.verify_email()
            login(self.request, user)
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_confirmed = True
        user.email_secret = ""
        user.save()
        # success message
    except models.User.DoesNotExist:
        # error message
        pass
    return redirect(reverse("core:home"))


def github_login(requset):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callbacK(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            req = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = req.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                api_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )

                profile_json = api_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    if email is None:
                        raise GithubException()
                    # bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            # first_name=name,
                            # bio=bio,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("core:home"))
