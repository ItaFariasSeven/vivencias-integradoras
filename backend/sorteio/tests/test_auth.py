from django.test import TestCase, override_settings

from sorteio.models import (
    Usuario,
    Aluno,
    Curso,
    Turno,
)

@override_settings(
    PASSWORD_HASHERS=[
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]
)
class AuthTests(TestCase):

    def setUp(self):

        self.usuario = Usuario.objects.create_user(
            username="teste@example.com",
            email="teste@example.com",
            first_name="Aluno",
            last_name="Teste",
            password="SenhaForte#2026"
        )

        self.aluno = Aluno.objects.create(
            usuario=self.usuario,
            ra="1000000001",
            data_nascimento="2000-01-01",
            curso=Curso.ADS,
            turno=Turno.NOTURNO
        )


    def test_usuario_criado(self):

        self.assertEqual(
            Usuario.objects.count(),
            1
        )

        self.assertEqual(
            Aluno.objects.count(),
            1
        )


    def test_senha_nao_fica_em_texto_puro(self):

        self.assertNotEqual(
            self.usuario.password,
            "SenhaForte#2026"
        )

        self.assertTrue(
            self.usuario.check_password(
                "SenhaForte#2026"
            )
        )


    def test_ra_unico(self):

        with self.assertRaises(Exception):

            Aluno.objects.create(
                usuario=Usuario.objects.create_user(
                    username="outro@example.com",
                    email="outro@example.com",
                    password="SenhaForte#2026"
                ),
                ra="1000000001",
                data_nascimento="2000-01-01",
                curso=Curso.PEDAGOGIA,
                turno=Turno.NOTURNO
            )