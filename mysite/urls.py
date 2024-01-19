
#                      ============== SITE MAIN URLS ================                               #
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views

urlpatterns = [
    path('The page of Peace/', admin.site.urls),
    path('',include('blog.urls')),
    path('accounts/login',views.LoginView.as_view(),name='login'),
    path('accounts/logout',views.LogoutView.as_view(),name='logout',kwargs={'next_page':'/'}), #when you logout, the next page you go to is the homepage ('/')
]
