from django.urls import path,include
from .views import (IndexView,LoginView,SignupView,LogoutView,UserProfileView,GetAllUrlsView)

urlpatterns = [

    path('',LoginView.as_view(),name="login_view"),
    path('signup/', SignupView.as_view(), name="sign_up_view"),
    path('index/', IndexView, name="index_view"),
    path('logout/', LogoutView.as_view(), name="logout_view"),
    path('user/profile/', UserProfileView, name="user_profile_view"),
    path('get/urls/', GetAllUrlsView.as_view(), name="get_all_urls_view")

]