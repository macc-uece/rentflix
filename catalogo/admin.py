from django.contrib import admin
from catalogo.models import Filme, Genero, FilmeInstancia, Diretor 


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_diplay = ('titulo', 'diretor', 'display_genero')

admin.site.register(Genero)
admin.site.register(Diretor)
