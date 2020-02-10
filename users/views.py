from django.shortcuts import render, reverse, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms

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
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "tongnamuu@naver.com"})
        return render(request, "users/login.html", {"form": form,})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("######login#########")
                return redirect(reverse("core:home"))
            else:
                print("Error")
        return render(request, "users/login.html", {"form": form,})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
