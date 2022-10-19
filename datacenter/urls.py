from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, RequestView, FileView , dropdownList, searchFile,downloadFile

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('request', RequestView.as_view()),
    path('upload', FileView.as_view({'post': 'create'}), name='file-upload'),
    path('dropdownlist', dropdownList),
    path('searchfile', searchFile),
    path('downloadFile', downloadFile),
]