from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username


class Raca(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    bonus_for = models.IntegerField(default=0, verbose_name="Bônus de Força")
    bonus_dex = models.IntegerField(default=0, verbose_name="Bônus de Destreza")
    bonus_con = models.IntegerField(default=0, verbose_name="Bônus de Constituição")
    bonus_int = models.IntegerField(default=0, verbose_name="Bônus de Inteligência")
    bonus_sab = models.IntegerField(default=0, verbose_name="Bônus de Sabedoria")
    bonus_car = models.IntegerField(default=0, verbose_name="Bônus de Carisma")
    imagem = models.ImageField(upload_to='racas/', blank=True, null=True)

    def __str__(self):
        return self.nome


class PassivaRacial(models.Model):
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name='passivas')
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome} ({self.raca.nome})"