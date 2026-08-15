"""
AstralCaos — Views de conta e personagem, adaptadas do djangoquest.

Mantém exatamente o MESMO fluxo do djangoquest (cadastro -> login ->
seleciona/cria personagem -> entra -> pode deletar), só trocando o model
`Personagem` (simples, classe fixa em string) pelo `Character` do AstralCaos
(raça + classe + 6 atributos).

Cole em game/views.py (ou equivalente no seu app).
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Character, CharacterClass, Race


# ---------------------------------------------------------------------------
# Página inicial — igual ao djangoquest: decide pra onde mandar o usuário.
# ---------------------------------------------------------------------------

def index(request):
    if request.user.is_authenticated:
        if Character.objects.filter(user=request.user).exists():
            return redirect("selecionar_personagem")
        return redirect("criar_personagem")
    return redirect("login")


# ---------------------------------------------------------------------------
# Cadastro
# ---------------------------------------------------------------------------

def cadastro(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        if User.objects.filter(username=usuario).exists():
            return render(request, "game/cadastro.html", {"erro": "Usuário já existe!"})
        User.objects.create_user(username=usuario, password=senha)
        return redirect("login")
    return render(request, "game/cadastro.html")


# ---------------------------------------------------------------------------
# Login / Logout
# ---------------------------------------------------------------------------

def login_view(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        user = authenticate(request, username=usuario, password=senha)
        if user:
            login(request, user)
            if Character.objects.filter(user=user).exists():
                return redirect("selecionar_personagem")
            return redirect("criar_personagem")
        return render(request, "game/login.html", {"erro": "Usuário ou senha inválidos."})
    return render(request, "game/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------------------------------------------------------
# Criar personagem
# ---------------------------------------------------------------------------

def criar_personagem(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        race = get_object_or_404(Race, id=request.POST["race_id"])
        primary_class = get_object_or_404(CharacterClass, id=request.POST["class_id"])

        personagem = Character(
            user=request.user,
            name=nome,
            race=race,
            primary_class=primary_class,
        )
        personagem.apply_starting_attributes()  # base + raça + classe
        personagem.save()

        request.session["personagem_id"] = personagem.id
        request.session.modified = True
        return redirect("mundo")

    # GET: manda pro template os dados pra montar os selects de raça/classe
    context = {
        "races": Race.objects.all(),
        "classes": CharacterClass.objects.filter(available_in_v1=True),
    }
    return render(request, "game/criar_personagem.html", context)


# ---------------------------------------------------------------------------
# Selecionar / entrar num personagem
# ---------------------------------------------------------------------------

def selecionar_personagem(request):
    personagens = Character.objects.filter(user=request.user)
    return render(request, "game/selecionar_personagem.html", {"personagens": personagens})


def entrar_personagem(request, personagem_id):
    personagem = get_object_or_404(Character, id=personagem_id, user=request.user)
    request.session["personagem_id"] = personagem.id
    request.session.modified = True
    return redirect("mundo")


# ---------------------------------------------------------------------------
# Deletar personagem
# ---------------------------------------------------------------------------

def deletar_personagem(request, personagem_id):
    if request.method == "POST":
        personagem = get_object_or_404(Character, id=personagem_id, user=request.user)
        if request.session.get("personagem_id") == personagem.id:
            del request.session["personagem_id"]
        personagem.delete()
    return redirect("selecionar_personagem")