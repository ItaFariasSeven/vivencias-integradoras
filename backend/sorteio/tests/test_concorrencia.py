from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.db import close_old_connections
from django.test import TransactionTestCase, override_settings

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


@override_settings(
    PASSWORD_HASHERS=[
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]
)
class ConcorrenciaSorteioTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self):

        self.edicao = EdicaoSorteio.objects.create(
            nome="Teste Concorrência",
            turno=Turno.NOTURNO,
            ativa=True,
        )

        # Cada grupo terá somente 1 vaga.
        # Capacidade total do eixo = 4.
        self.eixo = Eixo.objects.create(
            edicao=self.edicao,
            nome_eixo="Eixo Concorrência",
            ordem=1,
            quantidade_grupos=4,
            capacidade_grupo=1,
            ativo=True,
        )

        self.grupos = []

        for numero in range(1, 5):
            grupo = Grupo.objects.create(
                eixo=self.eixo,
                numero=numero,
            )

            self.grupos.append(grupo)

        # Ocupamos previamente 3 das 4 vagas.
        for numero in range(1, 4):

            aluno = self.criar_aluno(
                numero=numero,
                curso=Curso.ADS,
            )

            InscricaoSorteio.objects.create(
                aluno=aluno,
                edicao=self.edicao,
                eixo=self.eixo,
                grupo=self.grupos[numero - 1],
            )

        # Dois alunos disputarão a única vaga restante.
        self.aluno_a = self.criar_aluno(
            numero=100,
            curso=Curso.PEDAGOGIA,
        )

        self.aluno_b = self.criar_aluno(
            numero=101,
            curso=Curso.ENFERMAGEM,
        )


    def criar_aluno(self, numero, curso):

        usuario = Usuario.objects.create_user(
            username=f"concorrencia{numero}@teste.com",
            email=f"concorrencia{numero}@teste.com",
            first_name=f"Aluno{numero}",
            password="SenhaForte#2026",
        )

        return Aluno.objects.create(
            usuario=usuario,
            ra=f"{numero:010d}",
            data_nascimento="2000-01-01",
            curso=curso,
            turno=Turno.NOTURNO,
        )


    def test_dois_alunos_disputam_ultima_vaga(self):

        barreira = Barrier(2)

        eixo_id = self.eixo.id
        aluno_a_id = self.aluno_a.id
        aluno_b_id = self.aluno_b.id


        def tentar_sortear(aluno_id):

            # Cada thread precisa usar sua própria
            # conexão com o banco.
            close_old_connections()

            try:

                aluno = Aluno.objects.get(
                    pk=aluno_id
                )

                # Faz as duas threads chegarem
                # praticamente juntas ao sorteio.
                barreira.wait()

                inscricao, criado = (
                    sortear_aluno_noturno(
                        aluno=aluno,
                        eixo_id=eixo_id,
                    )
                )

                return {
                    "resultado": "sorteado",
                    "grupo_id": inscricao.grupo_id,
                    "criado": criado,
                }

            except SorteioSemVagas:

                return {
                    "resultado": "sem_vaga",
                }

            finally:

                close_old_connections()


        with ThreadPoolExecutor(
            max_workers=2
        ) as executor:

            futuro_a = executor.submit(
                tentar_sortear,
                aluno_a_id,
            )

            futuro_b = executor.submit(
                tentar_sortear,
                aluno_b_id,
            )

            resultados = [
                futuro_a.result(),
                futuro_b.result(),
            ]


        sorteados = [
            resultado
            for resultado in resultados
            if resultado["resultado"]
            == "sorteado"
        ]

        sem_vaga = [
            resultado
            for resultado in resultados
            if resultado["resultado"]
            == "sem_vaga"
        ]


        # Só UM dos dois pode ocupar a última vaga.
        self.assertEqual(
            len(sorteados),
            1,
        )

        self.assertEqual(
            len(sem_vaga),
            1,
        )


        # O eixo deve terminar exatamente com 4 alunos.
        total = (
            InscricaoSorteio.objects
            .filter(eixo=self.eixo)
            .count()
        )

        self.assertEqual(
            total,
            4,
        )


        # Nenhum grupo pode ultrapassar 1 vaga.
        for grupo in Grupo.objects.filter(
            eixo=self.eixo
        ):

            quantidade = (
                InscricaoSorteio.objects
                .filter(grupo=grupo)
                .count()
            )

            self.assertLessEqual(
                quantidade,
                1,
            )


        # O grupo 4, que era o único vazio,
        # deve terminar com exatamente um aluno.
        quantidade_grupo_4 = (
            InscricaoSorteio.objects
            .filter(
                grupo=self.grupos[3]
            )
            .count()
        )

        self.assertEqual(
            quantidade_grupo_4,
            1,
        )

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.db import close_old_connections
from django.test import TransactionTestCase, override_settings

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


@override_settings(
    PASSWORD_HASHERS=[
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]
)
class ConcorrenciaMuitosAlunosTests(
    TransactionTestCase
):

    reset_sequences = True


    def setUp(self):

        self.edicao = (
            EdicaoSorteio.objects.create(
                nome="Teste Concorrência Múltipla",
                turno=Turno.NOTURNO,
                ativa=True,
            )
        )


        self.eixo = Eixo.objects.create(
            edicao=self.edicao,
            nome_eixo="Eixo Concorrência",
            ordem=1,
            quantidade_grupos=4,
            capacidade_grupo=10,
            ativo=True,
        )


        self.grupos = []

        for numero in range(1, 5):

            grupo = Grupo.objects.create(
                eixo=self.eixo,
                numero=numero,
            )

            self.grupos.append(grupo)


        # Colocamos 8 alunos em cada grupo.
        # 4 grupos x 8 = 32 alunos.
        contador = 1

        for grupo in self.grupos:

            for _ in range(8):

                aluno = self.criar_aluno(
                    numero=contador,
                    curso=Curso.ADS,
                )

                InscricaoSorteio.objects.create(
                    aluno=aluno,
                    edicao=self.edicao,
                    eixo=self.eixo,
                    grupo=grupo,
                )

                contador += 1


        # Criamos 12 alunos para disputar
        # as 8 vagas que ainda existem.
        self.candidatos = []

        cursos = [
            Curso.ADS,
            Curso.PEDAGOGIA,
            Curso.ENFERMAGEM,
            Curso.DIREITO,
            Curso.PSICOLOGIA,
        ]


        for indice in range(12):

            aluno = self.criar_aluno(
                numero=100 + indice,
                curso=cursos[
                    indice % len(cursos)
                ],
            )

            self.candidatos.append(
                aluno
            )


    def criar_aluno(
        self,
        numero,
        curso
    ):

        usuario = Usuario.objects.create_user(
            username=(
                f"stress{numero}@teste.com"
            ),
            email=(
                f"stress{numero}@teste.com"
            ),
            first_name=f"Aluno{numero}",
            password="SenhaForte#2026",
        )


        return Aluno.objects.create(
            usuario=usuario,
            ra=f"{numero:010d}",
            data_nascimento="2000-01-01",
            curso=curso,
            turno=Turno.NOTURNO,
        )


    def test_varios_alunos_disputam_ultimas_vagas(
        self
    ):

        quantidade_candidatos = len(
            self.candidatos
        )

        barreira = Barrier(
            quantidade_candidatos
        )

        eixo_id = self.eixo.id

        aluno_ids = [
            aluno.id
            for aluno in self.candidatos
        ]


        def tentar_sortear(aluno_id):

            close_old_connections()

            try:

                aluno = Aluno.objects.get(
                    pk=aluno_id
                )


                # Todas as threads tentam chegar
                # aqui antes de iniciar o sorteio.
                barreira.wait()


                inscricao, criado = (
                    sortear_aluno_noturno(
                        aluno=aluno,
                        eixo_id=eixo_id,
                    )
                )


                return {
                    "resultado": "sorteado",
                    "aluno_id": aluno_id,
                    "grupo_id":
                        inscricao.grupo_id,
                    "criado": criado,
                }


            except SorteioSemVagas:

                return {
                    "resultado": "sem_vaga",
                    "aluno_id": aluno_id,
                }


            finally:

                close_old_connections()


        with ThreadPoolExecutor(
            max_workers=quantidade_candidatos
        ) as executor:

            futuros = [
                executor.submit(
                    tentar_sortear,
                    aluno_id
                )
                for aluno_id in aluno_ids
            ]


            resultados = [
                futuro.result()
                for futuro in futuros
            ]


        sorteados = [
            resultado
            for resultado in resultados
            if resultado["resultado"]
            == "sorteado"
        ]


        sem_vaga = [
            resultado
            for resultado in resultados
            if resultado["resultado"]
            == "sem_vaga"
        ]


        # Existiam somente 8 vagas.
        self.assertEqual(
            len(sorteados),
            8
        )


        # Dos 12 candidatos,
        # exatamente 4 devem ficar sem vaga.
        self.assertEqual(
            len(sem_vaga),
            4
        )


        # O eixo deve terminar exatamente cheio.
        total_eixo = (
            InscricaoSorteio.objects
            .filter(
                eixo=self.eixo
            )
            .count()
        )


        self.assertEqual(
            total_eixo,
            40
        )


        # Cada grupo deve terminar com 10,
        # nunca 11 ou mais.
        for grupo in Grupo.objects.filter(
            eixo=self.eixo
        ):

            quantidade = (
                InscricaoSorteio.objects
                .filter(
                    grupo=grupo
                )
                .count()
            )


            self.assertEqual(
                quantidade,
                10
            )


        # Nenhum candidato pode ter
        # mais de uma inscrição.
        for aluno_id in aluno_ids:

            quantidade = (
                InscricaoSorteio.objects
                .filter(
                    aluno_id=aluno_id
                )
                .count()
            )


            self.assertLessEqual(
                quantidade,
                1
            )


        # Os 8 sorteados precisam ser
        # 8 alunos diferentes.
        ids_sorteados = [
            resultado["aluno_id"]
            for resultado in sorteados
        ]


        self.assertEqual(
            len(ids_sorteados),
            len(set(ids_sorteados))
        )