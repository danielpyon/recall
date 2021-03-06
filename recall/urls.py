"""recall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.utils.decorators import method_decorator
from .views import SignupFormView, AnonOnlyMixin

class FixedPasswordResetView(AnonOnlyMixin, PasswordResetView):
    pass

class FixedPasswordResetConfirmView(AnonOnlyMixin, PasswordResetConfirmView):
    pass

urlpatterns = [
    path('', RedirectView.as_view(url='app/', permanent=True), name='app'),
    path('app/', include('app.urls')),
    path('accounts/signup/', SignupFormView.as_view(), name='signup'),

    # accessible only to anons
    path('accounts/login/', LoginView.as_view(redirect_authenticated_user=True)),
    path('accounts/password_reset/', FixedPasswordResetView.as_view()),
    path('accounts/password_confirm/', FixedPasswordResetConfirmView.as_view()),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
