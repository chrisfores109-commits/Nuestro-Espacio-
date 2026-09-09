from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pareja/crear/', views.crear_pareja, name='crear_pareja'),
    path('pareja/unirse/', views.unirse_pareja, name='unirse_pareja'),
    path('seccion/crear/', views.crear_seccion, name='crear_seccion'),
    path('notas/', views.notas, name='notas'),
    path('archivo/subir/', views.subir_archivo, name='subir_archivo'),
    path('archivo/<int:archivo_id>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('galeria/', views.galerias, name='galeria'),
]