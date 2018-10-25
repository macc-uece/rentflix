from django.shortcuts import render
from catalogo.models import Filme, Diretor, FilmeInstancia, Genero
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):

    num_filmes = Filme.objects.all().count()
    num_instancias = FilmeInstancia.objects.all().count()
    
    num_instancias_disponiveis = FilmeInstancia.objects.filter(status__exact='d').count()
    
    num_diretores = Diretor.objects.count()
    filmes_disponiveis = FilmeInstancia.objects.all().filter(status__exact='d')
    filmes = Filme.objects.all()

    
    context = {
        'num_filmes': num_filmes,
        'num_instancias': num_instancias,
        'num_instancias_disponiveis':  num_instancias_disponiveis,
        'num_diretores': num_diretores,
        'filmes_disponiveis': filmes_disponiveis,
        'filmes' : filmes,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@login_required
def alugar(request, filme_id):
    filme_escolhido = Filme.objects.all().filter(id__exact=filme_id)[0]
    context = {   
        'filme_escolhido' : filme_escolhido,
    }   
    return render(request, 'pagamento.html', context=context)


@login_required
def pagar(request, filme_id):
    filme_alugado = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme_alugado)
    
    filme_instancia.status = 'e'
    filme_instancia.save()
    
    #historico = HistoricoAluguel(id=filme_alugado.id, filme=filme_alugado.filme, usuario=self, data_devolucao=filme_alugado.data_devolucao)
    #historico.save()
    return redirect('index')


class FilmeListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view for a list of books.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Filme
    paginate_by = 10


class FilmeDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Filme


class DiretorListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Diretor
    paginate_by = 10 


class DiretorDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Diretor

class GeneroListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Genero
    paginate_by = 10 


class GeneroDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Genero

