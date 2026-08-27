from django.urls import path
from .views import CsrfView, CadastroAlunoView, LoginView, LogoutView, UsuarioAtualView, EixoListView, MeuGrupoView, SortearGrupoView, GruposDoEixoView

urlpatterns = [
    path('auth/csrf/', CsrfView.as_view(), name='csrf'),
    path('auth/cadastro/', CadastroAlunoView.as_view(), name='cadastro-aluno'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', UsuarioAtualView.as_view(), name='usuario-atual'),
    path('sorteio/eixos/', EixoListView.as_view(), name='eixos'),
    path('sorteio/sortear/', SortearGrupoView.as_view(), name='sortear'),
    path('sorteio/meu-grupo/', MeuGrupoView.as_view(), name='meu-grupo'),
    path('sorteio/eixos/<int:eixo_id>/grupos/', GruposDoEixoView.as_view(), name='grupos-do-eixo'),
]
