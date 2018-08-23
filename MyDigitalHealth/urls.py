from django.urls import path
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', login, {'template_name': 'login.html'}, name='login'),
    path('logout', logout, name='logout'),
    path('create', views.create, name='create'),
    path('register', views.register, name='register'),
    path('cards', views.cards, name='cards'),
    path('view', views.view, name='view'),
    path('package', views.package, name='package'),
    path('packageList/<package>/', views.packageList, name='packageList'),
    path('comments', views.comments, name='comments'),
    path('admin', views.admin, name='admin'),
    path('edit/<package>/', views.edit, name='edit'),
    path('editPackage/<package>/', views.editPackage, name='editPackage'),
]
