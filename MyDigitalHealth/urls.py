from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register', views.register, name='register_user'),
    path('create_package', views.create_package, name='create_package'),
    path('package_preview/<package_id>/', views.package_preview, name='package_preview'),
    path('view', views.view, name='view'),
    path('package', views.package, name='package'),
    path('open_package/<package_id>/', views.open_package, name='open_package'),
    path('comments', views.comments, name='comments'),
    path('admin', views.admin, name='admin'),
    path('edit/<package>/', views.edit, name='edit'),
    path('editPackage/<package_id>/', views.editPackage, name='editPackage'),
]
