from django.shortcuts import render
from catalogo.models import Filme, Diretor, FilmeInstancia, Genero, CustomUser
from catalogo.models import HistoricoAluguel, HistoricoFilmesAvaliacao, Comentario
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from .forms import ComentarioForm


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
def painel_admin(request):
    filmes = FilmeInstancia.objects.all()
    context = { 'filmes': filmes }
    return render(request, 'paineladmin.html', context=context)

@login_required
def top_alugados(request):
    filmes = FilmeInstancia.objects.all().filter().order_by('-alugado_number')
    context = { 'filmes': filmes }
    return render(request, 'topalugados.html', context=context)
    
@login_required
def top_usuarios(request):
    usuarios = CustomUser.objects.all().filter().order_by('-alugou')
    context = { 'usuarios': usuarios }
    return render(request, 'topusuarios.html', context=context)

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
    context = {
        'filme': filme,
        'filmeInstancia': filme_instancia,
    }
    return render(request, 'catalogo/add_avaliacao.html', context=context)
    
@login_required
def avaliado(request, filme_id):
    filme = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme)
    username_logado = get_perfil_logado(request)
    star = request.GET.get('star')
    print(star)
    if star == None :
        return render(request, 'catalogo/add_avaliacao.html', {"filme" : filme, "avaliado" : '0' })

    else :
        try:
            filme_avaliado = HistoricoFilmesAvaliacao.objects.get(usuario__exact=username_logado, filme__exact=filme_instancia.filme)
        except HistoricoFilmesAvaliacao.DoesNotExist:
            filme_avaliado = None

        context = {
            'filme': filme,
            'filme_avaliado': filme_avaliado,
            'filmeInstancia': filme_instancia
        }

        if filme_avaliado:
            print('entrei')
            if star == "5":
                filme_avaliado.classificacao ='5'
                filme_avaliado.save()


            if star == "4":
                filme_avaliado.classificacao ='4'
                filme_avaliado.save()


            if star == "3":
                filme_avaliado.classificacao ='3'
                filme_avaliado.save()


            if star == "2":
                filme_avaliado.classificacao ='2'
                filme_avaliado.save()


            if star == "1":
                filme_avaliado.classificacao ='1'
                filme_avaliado.save()

        else:

            filme_avaliado = HistoricoFilmesAvaliacao(filme=filme_instancia.filme, 
                    usuario=username_logado, classificacao=star)
            filme_avaliado.save()


        return redirect('detail_filme',  filme_id=filme.id)
    
@login_required
def pagar(request, filme_id):
    filme_alugado = Filme.objects.get(id__exact=filme_id)
    filme_instancia = FilmeInstancia.objects.get(filme__exact=filme_alugado)
    data_atual = date.today()
    data_devolucao = date.fromordinal(data_atual.toordinal()+7)
    username_logado = get_perfil_logado(request)
    
    filme_instancia.status = 'e'
    filme_instancia.data_devolucao = data_devolucao
    if filme_instancia.alugado_number == None:
        filme_instancia.alugado_number = 1
    else:
        filme_instancia.alugado_number = filme_instancia.alugado_number + 1
    filme_instancia.save()
   
    user = CustomUser.objects.get(username__exact = username_logado)
    user.alugou = user.alugou + 1
    user.gastou = user.gastou + 5
    user.save()

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
    num_filme_avaliado_1 = HistoricoFilmesAvaliacao.objects.all().filter(filme__exact=filme_instancia.filme).filter(classificacao__exact='1').count()
    num_filme_avaliado_2 = HistoricoFilmesAvaliacao.objects.all().filter(filme__exact=filme_instancia.filme).filter(classificacao__exact='2').count()
    num_filme_avaliado_3 = HistoricoFilmesAvaliacao.objects.all().filter(filme__exact=filme_instancia.filme).filter(classificacao__exact='3').count()
    num_filme_avaliado_4 = HistoricoFilmesAvaliacao.objects.all().filter(filme__exact=filme_instancia.filme).filter(classificacao__exact='4').count()
    num_filme_avaliado_5 = HistoricoFilmesAvaliacao.objects.all().filter(filme__exact=filme_instancia.filme).filter(classificacao__exact='5').count()
    if num_filme_avaliado_1 == 0 and num_filme_avaliado_2 == 0 and num_filme_avaliado_3 == 0 and num_filme_avaliado_4 == 0 and num_filme_avaliado_5 == 0 :
        media = 0

    else :
        media = ((num_filme_avaliado_1 * 1) + (num_filme_avaliado_2 * 2) + (num_filme_avaliado_3 * 3) + (num_filme_avaliado_4 * 4) + (num_filme_avaliado_5 * 5))/((num_filme_avaliado_1 + num_filme_avaliado_2 + num_filme_avaliado_3 + num_filme_avaliado_4 + num_filme_avaliado_5))

    print(num_filme_avaliado_1 * 1)
    print(num_filme_avaliado_2 * 2)
    print(num_filme_avaliado_3 * 3)
    print(num_filme_avaliado_4 * 4)
    print(num_filme_avaliado_5 * 5)
    print(media)
    if media > 0 and media <= 1.5 :
        filme.classificacao = '1' 
        filme.save()

    if media > 1.5 and media <= 2.5:
        filme.classificacao = '2' 
        filme.save() 

    if media > 2.5 and media <= 3.5:
        filme.classificacao = '3' 
        filme.save()

    if media > 3.5 and media <= 4.5:
        filme.classificacao = '4' 
        filme.save()

    if media > 4.5:
        filme.classificacao = '5' 
        filme.save()
    
    comentarios = Comentario.objects.all().filter(comentario__exact = filme_instancia)
    
    context = {
        'filme' : filme,
        'filmeInstancia': filme_instancia,
        'comentarios': comentarios,
    }

    return render(request, 'catalogo/filme_detail.html', context=context)
    
@ensure_csrf_cookie
@login_required
def comentar(request, filme_instancia):
    username_logado = get_perfil_logado(request)
    filmeInstancia = FilmeInstancia.objects.all().filter(id__exact = filme_instancia.split(" ")[0])
    
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.comentario = filmeInstancia[0]
            c.usuario = username_logado
            c.email = request.user.email
            c.save()
            return redirect('detail_filme', filme_id=filmeInstancia[0].filme.id)
    else:
        form = ComentarioForm()
    template = 'catalogo/add_comentario.html'
    context = {'form': form}
    return render(request, template, context)


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
