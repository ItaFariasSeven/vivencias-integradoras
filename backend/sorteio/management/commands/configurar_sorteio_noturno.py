from django.core.management.base import BaseCommand
from django.db import transaction
from sorteio.models import EdicaoSorteio, Eixo, Grupo, Turno

class Command(BaseCommand):
    help = 'configura a edição noturna com 10 eixos e 4 grupos por eixo.'

    @transaction.atomic
    def handle(self, *args, **options):
        edicao, criada = EdicaoSorteio.objects.get_or_create(
            nome='Vivências Integradoras 2026.2',
            turno=Turno.NOTURNO,
            defaults={
                'ativa': True
            }
        )

        if not edicao.ativa:
            edicao.ativa = True
            edicao.save(update_fields=['ativa'])

        for numero_eixo in range(1, 11):
            eixo, _ = Eixo.objects.update_or_create(
                edicao=edicao,
                ordem=numero_eixo,
                defaults={
                    'nome_eixo': f'Eixo{numero_eixo}',
                    'quantidade_grupos': 4,
                    'capacidade_grupo': 10,
                    'ativo': True,
                }
            )

            for numero_grupo in range(1, 5):
                Grupo.objects.get_or_create(
                    eixo=eixo,
                    numero=numero_grupo
                )

        self.stdout.write(
            self.style.SUCCESS(
                'sorteio noturno configurado com sucesso'
            )
        )

        self.stdout.write(
            f'Edição: {edicao.nome}'
        )

        self.stdout.write(
            f'Eixos: {edicao.eixos.count()}'
        )

        self.stdout.write(
            f'Grupos: {Grupo.objects.filter(eixo__edicao=edicao).count()}'
        )