from django.urls import path
from .import views
urlpatterns=[
    path('signupaccount/user',views.signupaccount, name='signupaccount'),
    path('signupaccount/admin',views.admin_signup, name='signupaccount_admin'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('login/', views.loginaccount, name='loginaccount'),
    path('adminpanel/', views.adminpanel, name="adminpanel"),
    path('adminlogin',views.admin_login, name="adminlogin"),
    path('adminpanel/createmovie', views.createmovie, name="createmovie"),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('allow_user/<int:user_id>/', views.allow_user, name='allow_user'),
    path('adminpanel/updatemovie/<int:movie_id>/', views.updatemovie, name="updatemovie"),
    path('adminpanel/deletemovie/<int:movie_id>/', views.deletemovie, name="deletemovie"),
]
