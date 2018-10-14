from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register', views.register, name='register'),
    path('create_package', views.create_package, name='create'),
    # path('packageList/<package>/', views.packageList, name='packageList'),
    path('active/<package_id>', views.cardsort_activity, name='active'),
    path('admin', views.package_administration, name='admin'),
    path('edit/<package_id>/', views.edit_package, name='edit'),
    # path('editPackage/<package>/', views.editPackage, name='editPackage'),
    path('delete/<package_id>', views.delete_package, name='delete'),
    path('css/<package_id>', views.get_css, name='css'),
]
