from django.contrib import admin
from catalogo.models import Filme, Genero, FilmeInstancia, Diretor, HistoricoAluguel, HistoricoFilmesAvaliacao


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_diplay = ('titulo', 'diretor', 'display_genero')

@admin.register(FilmeInstancia)
class FilmeInstanciaAdmin(admin.ModelAdmin):
    list_filter = ('status', 'data_devolucao')
    list_diplay = ('id', 'filme', 'data_devolucao', 'status')

admin.site.register(Genero)
admin.site.register(Diretor)
admin.site.register(HistoricoAluguel)
admin.site.register(HistoricoFilmesAvaliacao)
