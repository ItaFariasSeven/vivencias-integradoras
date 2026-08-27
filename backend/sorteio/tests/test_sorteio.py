from django.test import TestCase

from sorteio.models import (
    Usuario,
    Aluno,
    Curso,
    Turno,
    EdicaoSorteio,
    Eixo,
    Grupo,
    InscricaoSorteio,
)

from sorteio.services import (
    sortear_aluno_noturno,
    SorteioSemVagas,
)

from django.test import (
    TestCase,
    override_settings,
)

@override_settings(
    PASSWORD_HASHERS=[
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]
)
class SorteioTests(TestCase):

    def setUp(self):

        self.edicao = EdicaoSorteio.objects.create(
            nome="Teste Noturno",
            turno=Turno.NOTURNO,
            ativa=True
        )

        self.eixo = Eixo.objects.create(
            edicao=self.edicao,
            nome_eixo="Eixo Teste",
            ordem=1,
            quantidade_grupos=4,
            capacidade_grupo=10,
            ativo=True
        )

        for numero in range(1, 5):

            Grupo.objects.create(
                eixo=self.eixo,
                numero=numero
            )


    def criar_aluno(
        self,
        numero,
        curso
    ):

        usuario = Usuario.objects.create_user(
            username=f"aluno{numero}@teste.com",
            email=f"aluno{numero}@teste.com",
            first_name=f"Aluno{numero}",
            password="SenhaForte#2026"
        )

        return Aluno.objects.create(
            usuario=usuario,
            ra=f"{numero:010d}",
            data_nascimento="2000-01-01",
            curso=curso,
            turno=Turno.NOTURNO
        )


    def test_aluno_e_sorteado(self):

        aluno = self.criar_aluno(
            1,
            Curso.ADS
        )

        inscricao, criado = (
            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )
        )

        self.assertTrue(criado)

        self.assertEqual(
            inscricao.aluno,
            aluno
        )

        self.assertEqual(
            inscricao.eixo,
            self.eixo
        )

        self.assertIsNotNone(
            inscricao.grupo
        )


    def test_aluno_nao_pode_sortear_duas_vezes(self):

        aluno = self.criar_aluno(
            2,
            Curso.ADS
        )

        primeira, criado1 = (
            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )
        )

        segunda, criado2 = (
            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )
        )

        self.assertTrue(criado1)

        self.assertFalse(criado2)

        self.assertEqual(
            primeira.grupo_id,
            segunda.grupo_id
        )

        self.assertEqual(
            InscricaoSorteio.objects.filter(
                aluno=aluno
            ).count(),
            1
        )


    def test_grupo_nunca_ultrapassa_capacidade(self):

        alunos = []

        for numero in range(1, 41):

            alunos.append(
                self.criar_aluno(
                    numero,
                    Curso.ADS
                )
            )

        for aluno in alunos:

            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )

        grupos = Grupo.objects.filter(
            eixo=self.eixo
        )

        for grupo in grupos:

            total = (
                InscricaoSorteio.objects
                .filter(grupo=grupo)
                .count()
            )

            self.assertLessEqual(
                total,
                10
            )


    def test_eixo_cheio_rejeita_novo_aluno(self):

        for numero in range(1, 41):

            aluno = self.criar_aluno(
                numero,
                Curso.ADS
            )

            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )

        aluno_extra = self.criar_aluno(
            100,
            Curso.PEDAGOGIA
        )

        with self.assertRaises(
            SorteioSemVagas
        ):

            sortear_aluno_noturno(
                aluno=aluno_extra,
                eixo_id=self.eixo.id
            )

def test_distribui_mesmo_curso_entre_grupos(self):

    for numero in range(1, 9):

        aluno = self.criar_aluno(
            numero,
            Curso.ADS
        )

        sortear_aluno_noturno(
            aluno=aluno,
            eixo_id=self.eixo.id
        )


    quantidades = []

    for grupo in Grupo.objects.filter(
        eixo=self.eixo
    ):

        quantidade_ads = (
            InscricaoSorteio.objects
            .filter(
                grupo=grupo,
                aluno__curso=Curso.ADS
            )
            .count()
        )

        quantidades.append(
            quantidade_ads
        )


    diferenca = (
        max(quantidades) -
        min(quantidades)
    )


    self.assertLessEqual(
        diferenca,
        1
    )

def test_distribuicao_com_varios_cursos(self):

    cursos = [
        Curso.ADS,
        Curso.PEDAGOGIA,
        Curso.ENFERMAGEM,
        Curso.DIREITO,
        Curso.PSICOLOGIA,
    ]


    numero = 1

    for curso in cursos:

        for _ in range(4):

            aluno = self.criar_aluno(
                numero,
                curso
            )

            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )

            numero += 1


    grupos = Grupo.objects.filter(
        eixo=self.eixo
    )


    for grupo in grupos:

        total = (
            InscricaoSorteio.objects
            .filter(grupo=grupo)
            .count()
        )

        self.assertEqual(
            total,
            5
        )

def test_aluno_nao_muda_de_eixo_apos_sorteio(self):

    aluno = self.criar_aluno(
        1,
        Curso.ADS
    )

    primeiro, _ = (
        sortear_aluno_noturno(
            aluno=aluno,
            eixo_id=self.eixo.id
        )
    )


    outro_eixo = Eixo.objects.create(
        edicao=self.edicao,
        nome_eixo="Outro Eixo",
        ordem=2,
        quantidade_grupos=4,
        capacidade_grupo=10
    )


    for numero in range(1, 5):

        Grupo.objects.create(
            eixo=outro_eixo,
            numero=numero
        )


    segundo, criado = (
        sortear_aluno_noturno(
            aluno=aluno,
            eixo_id=outro_eixo.id
        )
    )


    self.assertFalse(criado)

    self.assertEqual(
        primeiro.eixo_id,
        segundo.eixo_id
    )

    self.assertEqual(
        primeiro.grupo_id,
        segundo.grupo_id
    )
    def test_mesmo_curso_fica_balanceado(self):

        for numero in range(1, 9):

            aluno = self.criar_aluno(
                numero,
                Curso.ADS
            )

            sortear_aluno_noturno(
                aluno=aluno,
                eixo_id=self.eixo.id
            )


        distribuicao = []

        for grupo in Grupo.objects.filter(
            eixo=self.eixo
        ):

            quantidade = (
                InscricaoSorteio.objects
                .filter(
                    grupo=grupo,
                    aluno__curso=Curso.ADS
                )
                .count()
            )

            distribuicao.append(
                quantidade
            )


        diferenca = (
            max(distribuicao) -
            min(distribuicao)
        )


        self.assertLessEqual(
            diferenca,
            1
        )

    def test_varios_cursos_ficam_distribuidos(self):

        cursos = [
            Curso.ADS,
            Curso.PEDAGOGIA,
            Curso.ENFERMAGEM,
            Curso.DIREITO,
            Curso.PSICOLOGIA,
        ]


        numero = 1


        for curso in cursos:

            for _ in range(4):

                aluno = self.criar_aluno(
                    numero,
                    curso
                )

                sortear_aluno_noturno(
                    aluno=aluno,
                    eixo_id=self.eixo.id
                )

                numero += 1


        for grupo in Grupo.objects.filter(
            eixo=self.eixo
        ):

            inscricoes = (
                InscricaoSorteio.objects
                .filter(grupo=grupo)
            )


            self.assertEqual(
                inscricoes.count(),
                5
            )


            for curso in cursos:

                quantidade = (
                    inscricoes
                    .filter(
                        aluno__curso=curso
                    )
                    .count()
                )


                self.assertEqual(
                    quantidade,
                    1
                )