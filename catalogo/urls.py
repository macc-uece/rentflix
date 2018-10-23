from django.urls import path
from catalogo import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('filmes/', views.FilmeListView.as_view(), name='filmes'),
   path('filme/<int:pk>', views.FilmeDetailView.as_view(), name='filme-info'),
   path('diretores/', views.DiretorListView.as_view(), name='diretores'),
   path('diretor/<int:pk>', views.DiretorDetailView.as_view(), name='diretor-info'),
]
