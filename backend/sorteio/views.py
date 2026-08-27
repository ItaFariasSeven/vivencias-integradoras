from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import ( authenticate, login, logout)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ( csrf_protect, ensure_csrf_cookie)
from rest_framework import status
from rest_framework.permissions import ( AllowAny, IsAuthenticated)
from rest_framework.exceptions import PermissionDenied
from .models import ( Aluno, EdicaoSorteio, Eixo, Grupo, InscricaoSorteio)
from .serializers import ( CadastroAlunoSerializer, LoginSerializer, EixoSerializer, GrupoSerializer, SorteioSerializer)
from .services import ( sortear_aluno_noturno, SorteioError)

from django.middleware.csrf import get_token

# Create your views here.

class TestView(APIView):

    def get(self, request):
        return Response({
            "Mensagem": "Backend Funcionando"
        })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        token = get_token(request)
        return Response({
            'mensagem': 'CSRF configurado',
            'csrfToken': token,
        })

@method_decorator(csrf_protect, name='dispatch')
class CadastroAlunoView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CadastroAlunoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aluno = serializer.save()
        return Response({
            'mensagem' : 'Cadastro Realizado com sucesso.',
            'aluno': {
                'nome' : aluno.usuario.get_full_name(),
                'email': aluno.usuario.email,
                'ra': aluno.ra,
                'curso': aluno.curso,
                'turno': aluno.turno
            }
        },
        status=status.HTTP_201_CREATED
    )

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ra = serializer.validated_data['ra']
        senha = serializer.validated_data['senha']

        try:
            aluno = (
                Aluno.objects.select_related('usuario').get(ra=ra)
            )
        except Aluno.DoesNotExist:
            return Response(
                {
                'erro': 'RA ou senha inválidos.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        usuario = authenticate(request=request, username=aluno.usuario.email, password=senha)

        if usuario is None:
            return Response(
                {
                    'erro': 'RA ou senha inválidos'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        login(request, usuario)

        return Response({
            'mensagem': 'Login realizado com sucesso',
            'usuario': {
                'nome': usuario.get_full_name(),
                'ra': aluno.ra,
                'curso': aluno.curso,
                'turno': aluno.turno
            }
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'mensagem': 'Logout realizado com sucesso'
        })

class UsuarioAtualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try: 
            aluno = request.user.perfil_aluno
        except Aluno.DoesNotExist:
            raise PermissionDenied('Este usuário não possui perfil de aluno')
        return Response({
            'id': request.user.id,
            'nome': request.user.get_full_name(),
            'email': request.user.email,
            'ra': aluno.ra,
            'curso': aluno.curso,
            'turno': aluno.turno
        })

class EixoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aluno = request.user.perfil_aluno
        edicao = get_object_or_404(EdicaoSorteio, turno=aluno.turno,ativa=True)
        eixos = Eixo.objects.filter(edicao=edicao, ativo=True)
        serializer = EixoSerializer(eixos, many=True)

        return Response(serializer.data)

class SortearGrupoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SorteioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aluno = request.user.perfil_aluno
        eixo_id = (serializer.validated_data['eixo_id'])

        try:
            inscricao, criado = (
                sortear_aluno_noturno(aluno=aluno, eixo_id=eixo_id)
            )
        except Eixo.DoesNotExist:
            return Response(
                {
                    'erro': 'Eixo Inválido'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except SorteioError as erro:
            return Response(
                {
                    'erro' : str(erro)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'novo_sorteio': criado,
            'eixo': {
                'id': inscricao.eixo.id,
                'nome': inscricao.eixo.nome_eixo
            },
            'grupo': {
                'id': inscricao.grupo.id,
                'nome': inscricao.grupo.nome
            }
        })

class MeuGrupoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aluno = request.user.perfil_aluno
        inscricao = (InscricaoSorteio.objects.filter(aluno=aluno, edicao__ativa=True).select_related('grupo', 'eixo').first())
        if not inscricao:
            return Response(
                {
                    'grupo': None
                }
            )
        grupo = (Grupo.objects.prefetch_related('inscricoes__aluno__usuario').get(pk=inscricao.grupo_id))
        serializer = GrupoSerializer(grupo)

        return Response({
            'eixo': {
                'id': inscricao.eixo.id,
                'nome': inscricao.eixo.nome_eixo
            },
            'grupo': serializer.data
        })


class GruposDoEixoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, eixo_id):
        aluno = request.user.perfil_aluno
        eixo = get_object_or_404(Eixo, pk=eixo_id, edicao__ativa=True)
        pertente_ao_eixo = (
            InscricaoSorteio.objects.filter(aluno=aluno, eixo=eixo).exists()
        )

        if not pertente_ao_eixo:
            raise PermissionDenied('Você não pertence a esse eixo')
        grupos = (Grupo.objects.filter(eixo=eixo).prefetch_related('inscricoes__aluno__usuario'))
        serializer = GrupoSerializer(grupos, many=True)
        return Response({
            'eixo': {
                'id': eixo.id,
                'nome':eixo.nome_eixo
            },
            'grupos': serializer.data
        })