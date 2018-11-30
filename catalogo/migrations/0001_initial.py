# Generated by Django 2.1.2 on 2018-11-30 00:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('conteudo', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diretor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('sinopse', models.TextField(help_text='Escreva um                                         pequeno sumário sobre o filme.', max_length=1000)),
                ('poster', models.ImageField(upload_to='posters/')),
                ('diretor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogo.Diretor')),
            ],
        ),
        migrations.CreateModel(
            name='FilmeInstancia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único para um filme no estoque', primary_key=True, serialize=False)),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('alugado_number', models.IntegerField()),
                ('status', models.CharField(blank=True, choices=[('m', 'Manutenção'), ('e', 'Emprestado'), ('d', 'Disponível'), ('r', 'Reservado')], default='m', help_text='Status do Filme', max_length=1)),
                ('filme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogo.Filme')),
            ],
            options={
                'ordering': ['data_devolucao'],
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Escreva um gênero                                         de um filme (i.e Ação)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoAluguel',
            fields=[
                ('id', models.UUIDField(default='uuid.uuid', primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=200)),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('data_aluguel', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Manutenção'), ('e', 'Emprestado'), ('d', 'Disponível'), ('r', 'Reservado')], default='m', max_length=1)),
                ('filme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogo.Filme')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoFilmesAvaliacao',
            fields=[
                ('id', models.UUIDField(default='uuid.uuid', primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=200)),
                ('classificacao', models.CharField(blank=True, choices=[('0', 'Nao-classificado'), ('1', '1 Estrela'), ('2', '2 Estrela'), ('3', '3 Estrela'), ('4', '4 Estrela'), ('5', '5 Estrela')], default='0', max_length=1)),
                ('filme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogo.Filme')),
            ],
        ),
        migrations.AddField(
            model_name='filme',
            name='genero',
            field=models.ManyToManyField(help_text='Escolha um gênero                                         para esse filme.', to='catalogo.Genero'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='comentario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comentarios', to='catalogo.FilmeInstancia'),
        ),
    ]
