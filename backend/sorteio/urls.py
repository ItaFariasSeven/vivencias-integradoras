from django.urls import path
from .views import CsrfView, CadastroAlunoView, LoginView, LogoutView, UsuarioAtualView, EixoListView, MeuGrupoView, SortearGrupoView, GruposDoEixoView

urlpatterns = [
    path('auth/csrf/', CsrfView.as_view()),
    path('auth/cadastro/', CadastroAlunoView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/me/', UsuarioAtualView.as_view()),
    path('sorteio/eixos/', EixoListView.as_view()),
    path('sorteio/sortear/', SortearGrupoView.as_view()),
    path('sorteio/meu-grupo/', MeuGrupoView.as_view()),
    path('sorteio/eixos/<int:eixo_id>/grupos', GruposDoEixoView.as_view()),
]
