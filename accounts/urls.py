from django.urls import path
from .import views
urlpatterns=[
    path('signupaccount/user',views.signupaccount, name='signupaccount'),
    path('signupaccount/admin',views.admin_signup, name='signupaccount_admin'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('login/', views.loginaccount, name='loginaccount'),
    path('adminpanel/', views.adminpanel, name="adminpanel"),
    path('adminlogin',views.admin_login, name="adminlogin"),
]