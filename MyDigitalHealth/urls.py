from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('create', views.create, name='create'),
    path('register', views.register, name='register'),
    path('cards', views.cards, name='cards'),
    path('view', views.view, name='view'),
    path('package', views.package, name='package'),
    path('packageList/<package>/', views.packageList, name='packageList'),
    path('comments/<package>', views.comments, name='comments'),
    path('admin', views.admin, name='admin'),
    path('edit/<package>/', views.edit, name='edit'),
    path('editPackage/<package>/', views.editPackage, name='editPackage'),
    path('deletePackage/<package_id>', views.deletePackage, name='deletePackage'),
]
