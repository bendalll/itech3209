from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register', views.register, name='register'),
    path('create_package', views.create_package, name='create_package'),
    path('admin', views.package_administration, name='admin'),
    path('edit_package/<package_id>/', views.edit_package, name='edit_package'),
    path('edit_save/<package_id>/', views.edit_save, name='edit_save'),
    path('preview/<package_id>/', views.package_preview, name='preview'),
    path('assign/<package_id>/', views.assign_choose_user, name="assign"),
    path('assign_to/<package_id>/<user_id>/', views.assign_package_to_user, name='assign_to'),
    path('delete/<package_id>/', views.delete_package, name='delete'),
    path('save/<package_id>/', views.save, name='save'),
]
