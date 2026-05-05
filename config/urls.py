from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('',                                         include('apps.restore.urls')),
  path('password-reset/',                          auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

  path('admin/', admin.site.urls),
  path('', include('admin_black.urls')),
]

try:
  urlpatterns.append( path("api/"      , include("api.urls"))    )
  urlpatterns.append( path("login/jwt/", view=obtain_auth_token) )
except:
  pass