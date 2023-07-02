from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='page-register'),
    path('login/', views.UserLoginView.as_view(), name='page-login'),
    path('logout/', views.UserLogoutView.as_view(), name='page-logout'),
    path('profile/<int:pk>/', include([
        path('', views.UserDetailsView.as_view(), name='profile-page'),
        path('edit/', views.UserEditView.as_view(), name='profile-edit'),
        path('delete/', views.UserDeleteView.as_view(), name='profile-delete'),
    ]))
]