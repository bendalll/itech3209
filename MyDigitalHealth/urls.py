from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register', views.register, name='register_user'),
    path('create_package', views.create_package, name='create_package'),
    path('preview', views.preview_package, name='preview'),
    path('cards', views.cards, name='cards'),
    path('view', views.view, name='view'),
    path('package', views.package, name='package'),
    path('packageList/<package>/', views.packageList, name='packageList'),
    path('comments', views.comments, name='comments'),
    path('admin', views.admin, name='admin'),
    path('edit/<package>/', views.edit, name='edit'),
    path('editPackage/<package_id>/', views.editPackage, name='editPackage'),
]
