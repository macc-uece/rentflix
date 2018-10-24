from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Genero(models.Model):
    """ Este modelo representa um gênero de um filme """
    nome = models.CharField(max_length = 200, help_text = "Escreva um gênero \
                                        de um filme (i.e Ação)")

    def __str__(self):
        """ String representando o modelo do objeto """
        return self.nome

    def get_absolute_url(self):
        """ Retorna uma URL para acessar os detalhes de um diretor """
        return reverse('genero-info', args = [str(self.id)])


class Filme(models.Model):
    """ Este modelo represeta um filme que pode ser alugado """
    titulo = models.CharField(max_length = 200)
    diretor = models.ForeignKey('Diretor', on_delete = models.SET_NULL, null =
            True)
    
    sinopse = models.TextField(max_length = 1000, help_text = 'Escreva um \
                                        pequeno sumário sobre o filme.')
    poster = models.ImageField(upload_to = 'posters/')
    
    genero = models.ManyToManyField(Genero, help_text = 'Escolha um gênero \
                                        para esse filme.')

    
    def __str__(self):
        """ String representando o modelo do objeto """
        return self.titulo

    def get_absolute_url(self):
        """ Retorna a URL para acessar os detalhes de um filme """
        return reverse('filme-info', args = [str(self.id)])
    
    def display_genero(self):
        """ Cria uma string para o gênero """
        return ', '.join(genero.nome for genero in self.genero.all()[:3])
    
    display_genero.short_description = 'Genero'


class FilmeInstancia(models.Model):
    """ Este modelo representa uma cópia do um filme """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text =
            'ID único para um filme no estoque')
    filme = models.ForeignKey('Filme', on_delete = models.SET_NULL, null = True)
    data_devolucao = models.DateField(null = True, blank = True)

    STATUS_EMPRESTIMO = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length = 1,
        choices = STATUS_EMPRESTIMO,
        blank = True,
        default = 'm',
        help_text = 'Status do Filme'
    )

    class Meta:
        ordering = ['data_devolucao']

    def __str__(self):
        """ String representando o modelo do objeto """
        return f"{self.id} ({self.filme.titulo})"

class Diretor(models.Model):
    """ Este modelo represente um diretor de um filme """
    nome = models.CharField(max_length = 200)

    def get_absolute_url(self):
        """ Retorna uma URL para acessar os detalhes de um diretor """
        return reverse('diretor-info', args = [str(self.id)])

    def __str__(self):
        """ String representando o modelo do objeto """
        return self.nome
    
