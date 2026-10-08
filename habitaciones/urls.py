from django.urls import path
from . import views
app_name = 'habitaciones'
urlpatterns = [path('', views.inicio, name='inicio'), path('habitaciones/', views.listado, name='listado'),
 path('habitaciones/crear/', views.crear, name='crear'), path('habitaciones/<int:pk>/', views.detalle, name='detalle'),
 path('habitaciones/<int:pk>/editar/', views.editar, name='editar'), path('habitaciones/<int:pk>/eliminar/', views.eliminar, name='eliminar')]
