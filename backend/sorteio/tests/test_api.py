from django.test import TestCase, override_settings
from django.urls import reverse

from rest_framework.test import APIClient

from sorteio.models import (
    Usuario,
    Aluno,
    Curso,
    Turno,
    EdicaoSorteio,
    Eixo,
    Grupo,
)


FAST_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher"
]


@override_settings(
    PASSWORD_HASHERS=FAST_HASHERS
)
class ApiSegurancaTests(TestCase):

    def setUp(self):

        self.senha = "SenhaForte#2026"

        self.usuario = Usuario.objects.create_user(
            username="aluno@teste.com",
            email="aluno@teste.com",
            first_name="Aluno",
            last_name="Teste",
            password=self.senha,
        )

        self.aluno = Aluno.objects.create(
            usuario=self.usuario,
            ra="2000000001",
            data_nascimento="2000-01-01",
            curso=Curso.ADS,
            turno=Turno.NOTURNO,
        )

        self.edicao = EdicaoSorteio.objects.create(
            nome="Teste API",
            turno=Turno.NOTURNO,
            ativa=True,
        )

        self.eixo1 = Eixo.objects.create(
            edicao=self.edicao,
            nome_eixo="Eixo 1",
            ordem=1,
            quantidade_grupos=4,
            capacidade_grupo=10,
            ativo=True,
        )

        self.eixo2 = Eixo.objects.create(
            edicao=self.edicao,
            nome_eixo="Eixo 2",
            ordem=2,
            quantidade_grupos=4,
            capacidade_grupo=10,
            ativo=True,
        )

        for eixo in [self.eixo1, self.eixo2]:
            for numero in range(1, 5):
                Grupo.objects.create(
                    eixo=eixo,
                    numero=numero,
                )


    def fazer_login(self):

        return self.client.post(
            reverse("login"),
            {
                "ra": self.aluno.ra,
                "senha": self.senha,
            },
            format="json",
        )


    def test_api_privada_rejeita_usuario_deslogado(self):

        resposta = self.client.get(
            reverse("eixos")
        )

        self.assertEqual(
            resposta.status_code,
            403
        )


    def test_login_com_senha_errada(self):

        resposta = self.client.post(
            reverse("login"),
            {
                "ra": self.aluno.ra,
                "senha": "senha-errada",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            401
        )


    def test_login_com_ra_inexistente(self):

        resposta = self.client.post(
            reverse("login"),
            {
                "ra": "9999999999",
                "senha": self.senha,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            401
        )


    def test_sortear_sem_eixo(self):

        self.fazer_login()

        resposta = self.client.post(
            reverse("sortear"),
            {},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            400
        )


    def test_sortear_eixo_inexistente(self):

        self.fazer_login()

        resposta = self.client.post(
            reverse("sortear"),
            {
                "eixo_id": 999999
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            404
        )


    def test_nao_visualiza_outro_eixo(self):

        self.fazer_login()

        sorteio = self.client.post(
            reverse("sortear"),
            {
                "eixo_id": self.eixo1.id
            },
            format="json",
        )

        self.assertEqual(
            sorteio.status_code,
            200
        )

        resposta = self.client.get(
            reverse(
                "grupos-do-eixo",
                kwargs={
                    "eixo_id": self.eixo2.id
                }
            )
        )

        self.assertEqual(
            resposta.status_code,
            403
        )


    def test_cadastro_rejeita_email_duplicado(self):

        resposta = self.client.post(
            reverse("cadastro-aluno"),
            {
                "nome": "Outro",
                "sobrenome": "Aluno",
                "email": self.usuario.email,
                "ra": "2000000002",
                "data_nascimento": "2001-01-01",
                "curso": "PEDAGOGIA",
                "turno": "NOTURNO",
                "senha": "OutraSenha#2026",
                "confirmar_senha": "OutraSenha#2026",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            400
        )

        self.assertIn(
            "email",
            resposta.data
        )


    def test_cadastro_rejeita_ra_duplicado(self):

        resposta = self.client.post(
            reverse("cadastro-aluno"),
            {
                "nome": "Outro",
                "sobrenome": "Aluno",
                "email": "outro@teste.com",
                "ra": self.aluno.ra,
                "data_nascimento": "2001-01-01",
                "curso": "PEDAGOGIA",
                "turno": "NOTURNO",
                "senha": "OutraSenha#2026",
                "confirmar_senha": "OutraSenha#2026",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            400
        )

        self.assertIn(
            "ra",
            resposta.data
        )


    def test_cadastro_rejeita_curso_invalido(self):

        resposta = self.client.post(
            reverse("cadastro-aluno"),
            {
                "nome": "Curso",
                "sobrenome": "Inválido",
                "email": "curso@teste.com",
                "ra": "2000000003",
                "data_nascimento": "2001-01-01",
                "curso": "HACKER",
                "turno": "NOTURNO",
                "senha": "OutraSenha#2026",
                "confirmar_senha": "OutraSenha#2026",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            400
        )

        self.assertIn(
            "curso",
            resposta.data
        )


    def test_cadastro_rejeita_turno_invalido(self):

        resposta = self.client.post(
            reverse("cadastro-aluno"),
            {
                "nome": "Turno",
                "sobrenome": "Inválido",
                "email": "turno@teste.com",
                "ra": "2000000004",
                "data_nascimento": "2001-01-01",
                "curso": "ADS",
                "turno": "MADRUGADA",
                "senha": "OutraSenha#2026",
                "confirmar_senha": "OutraSenha#2026",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            400
        )

        self.assertIn(
            "turno",
            resposta.data
        )


    def test_logout_realmente_encerra_sessao(self):

        login = self.fazer_login()

        self.assertEqual(
            login.status_code,
            200
        )

        antes = self.client.get(
            reverse("usuario-atual")
        )

        self.assertEqual(
            antes.status_code,
            200
        )

        logout = self.client.post(
            reverse("logout")
        )

        self.assertEqual(
            logout.status_code,
            200
        )

        depois = self.client.get(
            reverse("usuario-atual")
        )

        self.assertEqual(
            depois.status_code,
            403
        )

    def test_login_exige_csrf(self):

        client = APIClient(
            enforce_csrf_checks=True
        )

        csrf = client.get(
            reverse("csrf")
        )

        self.assertEqual(
            csrf.status_code,
            200
        )

        token = (
            client.cookies["csrftoken"].value
        )

        sem_token = client.post(
            reverse("login"),
            {
                "ra": self.aluno.ra,
                "senha": self.senha,
            },
            format="json",
        )

        self.assertEqual(
            sem_token.status_code,
            403
        )


        com_token = client.post(
            reverse("login"),
            {
                "ra": self.aluno.ra,
                "senha": self.senha,
            },
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            com_token.status_code,
            200
        )