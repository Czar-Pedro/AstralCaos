from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

#from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("", views.index, name="index"),
    #path("cadastro/", views.cadastro, name="cadastro"),
    #path("login/", views.login_view, name="login"),
    #path("logout/", views.logout_view, name="logout"),
    #path("criar-personagem/", views.criar_personagem, name="criar_personagem"),
    #path("selecionar-personagem/", views.selecionar_personagem, name="selecionar_personagem"),
    #path("entrar-personagem/<int:personagem_id>/", views.entrar_personagem, name="entrar_personagem"),
    #path("deletar-personagem/<int:personagem_id>/", views.deletar_personagem, name="deletar_personagem"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)