from django.urls import path
from catalogo import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('filmes/', views.FilmeListView.as_view(), name='filmes'),
   path('filme/<int:pk>', views.FilmeDetailView.as_view(), name='filme-info'),
   path('diretores/', views.DiretorListView.as_view(), name='diretores'),
   path('diretor/<int:pk>', views.DiretorDetailView.as_view(), name='diretor-info'),
   path('generos/', views.GeneroListView.as_view(), name='generos'),
   path('genero/<int:pk>', views.GeneroDetailView.as_view(), name='genero-info'),
   path('pagar/', views.pagar, name='pagar'), 
   path('alugar/', views.alugar, name='alugar'), 
]
