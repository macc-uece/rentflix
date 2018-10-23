from django.shortcuts import render
from catalogo.models import Filme, Diretor, FilmeInstancia, Genero

def index(request):

    num_filmes = Filme.objects.all().count()
    num_instancias = FilmeInstancia.objects.all().count()
    

    num_instancias_disponiveis = FilmeInstancia.objects.filter(status__exact='d').count()
    
    # The 'all()' is implied by default.    
    num_diretores = Diretor.objects.count()
    
    context = {
        'num_filmes': num_filmes,
        'num_instancias': num_instancias,
        'num_instancias_disponiveis':  num_instancias_disponiveis,
        'num_diretores': num_diretores,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
