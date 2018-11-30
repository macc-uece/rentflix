from django.contrib import admin
from catalogo.models import Filme, Genero, FilmeInstancia, Comentario
from catalogo.models import Diretor, HistoricoAluguel, HistoricoFilmesAvaliacao

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_diplay = ('titulo', 'diretor', 'display_genero')

@admin.register(FilmeInstancia)
class FilmeInstanciaAdmin(admin.ModelAdmin):
    exclude = ('alugado_number',)
    list_filter = ('status', 'data_devolucao')
    list_diplay = ('id', 'filme', 'data_devolucao', 'status')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_diplay = ['usuario', 'email']

admin.site.register(Genero)
admin.site.register(Diretor)
admin.site.register(HistoricoAluguel)
admin.site.register(HistoricoFilmesAvaliacao)
