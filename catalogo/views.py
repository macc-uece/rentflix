from django.shortcuts import render
from catalogo.models import Filme, Diretor, FilmeInstancia, Genero, HistoricoAluguel, HistoricoFilmesAvaliacao
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date



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
def pesquisar(request):
    filmesPesquisados = request.GET.get('palavra')
    opcao = request.GET.get('opcao')

    if opcao == "Filme" or opcao== None:
        list_filme_titulo = Filme.objects.all().filter(titulo__contains=filmesPesquisados)
        context = {   
            'list_filme_titulo' : list_filme_titulo,
            'filmesPesquisados' : filmesPesquisados,
            'opcao' : opcao

        }   
        return render(request, 'pesquisados.html', context=context)

    if opcao == "Genero":
        list_filme_genero = Filme.objects.all().filter(genero__nome__contains=filmesPesquisados)
        context = {   
            'list_filme_genero' : list_filme_genero,
            'filmesPesquisados' : filmesPesquisados,
            'opcao' : opcao

        }   
        return render(request, 'pesquisados.html', context=context)

    if opcao == "Diretor":
        list_filme_diretor = Filme.objects.all().filter(diretor__nome__contains=filmesPesquisados)
        print(list_filme_diretor)
        context = {   
            'list_filme_diretor' : list_filme_diretor,
            'filmesPesquisados' : filmesPesquisados,
            'opcao' : opcao

        }   
        return render(request, 'pesquisados.html', context=context)

    
    return render(request, 'pesquisados.html')
    
@login_required
def avaliar(request, filme_id):
    filme = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme)
    username_logado = get_perfil_logado(request)
    star = request.GET.get('star')
    try:
        filme_avaliado = HistoricoFilmesAvaliacao.objects.get(usuario__exact=username_logado, id__exact=filme_instancia.id)
    except HistoricoFilmesAvaliacao.DoesNotExist:
        filme_avaliado = None

    if filme_avaliado:
        if star == "5":
            filme_avaliado.classificacao ='5'
            filme_avaliado.save()
            context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
            return render(request, 'catalogo/filme_detail.html', context=context)

        if star == "4":
            filme_avaliado.classificacao ='4'
            filme_avaliado.save()
            context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
            return render(request, 'catalogo/filme_detail.html', context=context)

        if star == "3":
            filme_avaliado.classificacao ='3'
            filme_avaliado.save()
            context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
            return render(request, 'catalogo/filme_detail.html', context=context)

        if star == "2":
            filme_avaliado.classificacao ='2'
            filme_avaliado.save()
            context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
            return render(request, 'catalogo/filme_detail.html', context=context)

        if star == "1":
            filme_avaliado.classificacao ='1'
            filme_avaliado.save()
            context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
            return render(request, 'catalogo/filme_detail.html', context=context)
    else:

        filme_avaliado = HistoricoFilmesAvaliacao(id=filme_instancia.id, filme=filme_instancia.filme, 
                usuario=username_logado, classificacao=star)
        filme_avaliado.save()
        context = {   
                'filme' : filme,
                'filme_avaliado' : filme_avaliado,

            }   
        return render(request, 'catalogo/filme_detail.html', context=context)

    return redirect(request, 'catalogo/filme_detail.html', context=context)
    
@login_required
def pagar(request, filme_id):
    filme_alugado = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme_alugado)
    data_atual = date.today()
    data_devolucao = date.fromordinal(data_atual.toordinal()+7)
    username_logado = get_perfil_logado(request)
    
    filme_instancia.status = 'e'
    filme_instancia.data_devolucao = data_devolucao
    filme_instancia.save()
    
    historico = HistoricoAluguel(id=filme_instancia.id, filme=filme_instancia.filme, usuario=username_logado, 
        data_devolucao=data_devolucao, data_aluguel=data_atual, status=filme_instancia.status)
    historico.save()
    return redirect('index')

@login_required
def get_perfil_logado(request):
    return request.user.username

@login_required
def filmes(request):
    return render(request, 'catalogo/filme_list.html', {"filme_list" : Filme.objects.all()})

@login_required
def diretores(request):
    return render(request, 'catalogo/diretor_list.html', {"diretor_list" : Diretor.objects.all()})

@login_required
def generos(request):
    return render(request, 'catalogo/genero_list.html', {"genero_list" : Genero.objects.all()})

@login_required
def detail_filme(request, filme_id):
    filme = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme)
    username_logado = get_perfil_logado(request)
    try:
        filme_avaliado = HistoricoFilmesAvaliacao.objects.get(usuario__exact=username_logado, id__exact=filme_instancia.id)
    except HistoricoFilmesAvaliacao.DoesNotExist:
        filme_avaliado = None
    

    if filme_avaliado :
        context = {
            'filme' : filme,
            'username_logado' : username_logado,
            'filme_avaliado' : filme_avaliado,
        }
        return render(request, 'catalogo/filme_detail.html', context=context)
    return render(request, 'catalogo/filme_detail.html', {"filme" : filme})

@login_required
def detail_diretor(request, diretor_nome):
    diretor_escolhido = Diretor.objects.get(nome__exact=diretor_nome)
    filmes_dirigidos = Filme.objects.all().filter(diretor__exact=diretor_escolhido)
    context = {   
        'diretor_escolhido': diretor_escolhido,
        'filmes_dirigidos' : filmes_dirigidos,
        'diretor_nome': diretor_nome,
    }   
    return render(request, 'catalogo/diretor_detail.html', context=context)

@login_required
def detail_genero(request, genero_nome):
    genero_escolhido = Genero.objects.get(nome__exact=genero_nome)
    filmes_relacionados = Filme.objects.all().filter(genero__exact=genero_escolhido)
    context = {   
        'genero_escolhido': genero_escolhido,
        'filmes_relacionados' : filmes_relacionados,
        'genero_nome': genero_nome,
    }   
    return render(request, 'catalogo/genero_detail.html', context=context)

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