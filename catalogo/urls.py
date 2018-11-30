from django.urls import path
from catalogo import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('paineladmin/', views.painel_admin, name='painel_admin'), 
   path('topalugados/', views.top_alugados, name='top_alugados'),
   path('diretores/', views.diretores, name='diretores'),
   path('diretor/<diretor_nome>', views.detail_diretor, name='detail_diretor'),
   path('generos/', views.generos, name='generos'),
   path('genero/<genero_nome>', views.detail_genero, name='detail_genero'),
   path('alugar/<int:filme_id>', views.alugar, name='alugar'), 
   path('pagar/<int:filme_id>', views.pagar, name='pagar'),
   path('pesquisar/', views.pesquisar, name='pesquisar'),
   path('avaliar/<int:filme_id>/', views.avaliar, name='avaliar'),
   path('comentar/<filme_instancia>', views.comentar, name='comentar'),
   path('filmes/', views.filmes, name='filmes'),
   path('filme/<int:filme_id>/', views.detail_filme, name='detail_filme'),

]
