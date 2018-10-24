from django.shortcuts import render
from catalogo.models import Filme, Diretor, FilmeInstancia, Genero


def index(request):

    num_filmes = Filme.objects.all().count()
    num_instancias = FilmeInstancia.objects.all().count()
    

    num_instancias_disponiveis = FilmeInstancia.objects.filter(status__exact='d').count()
    
    # The 'all()' is implied by default.    
    num_diretores = Diretor.objects.count()
    filmesDisponiveis = FilmeInstancia.objects.all().filter(status__exact='d')
    filmes = Filme.objects.all()

    
    context = {
        'num_filmes': num_filmes,
        'num_instancias': num_instancias,
        'num_instancias_disponiveis':  num_instancias_disponiveis,
        'num_diretores': num_diretores,
        'filmesDisponiveis': filmesDisponiveis,
        'filmes' : filmes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def pagar(request):
    filmeEscolhido= Filme.objects.all().filter(titulo__exact='Jumanji')
    context = {
       
        'filmeEscolhido' : filmeEscolhido,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'pagamento.html', context=context)

def alugar(request, filme_titulo):
    filmeEscolhido= Filme.objects.all().filter(titulo__exact=filme_titulo)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.alugarFilme(filmeEscolhido)
    return redirect('pagar')

def get_perfil_logado(request):
    return request.user.perfil


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

class GeneroListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Genero
    paginate_by = 10 


class GeneroDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Genero

