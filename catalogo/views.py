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

from django.views import generic


class FilmeListView(generic.ListView):
    """
    Generic class-based view for a list of books.
    """
    model = Filme
    paginate_by = 10
    
class FilmeDetailView(generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    model = Filme

class DiretorListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Diretor
    paginate_by = 10 


class DiretorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Diretor