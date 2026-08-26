import secrets

from django.db import transaction
from django.db.models import Count, Q

from .models import Aluno, Eixo, Grupo, InscricaoSorteio, Turno

class SorteioError(Exception):
    pass

class SorteioSemVagas(SorteioError):
    pass

class SorteioConfiguracaoInvalida(SorteioError):
    pass

@transaction.atomic
def sortear_aluno_noturno(
    *,
    aluno: Aluno,
    eixo_id: int 
):
    # Bloquear aluno durante sorteio
    aluno = (
        Aluno.objects.select_for_update().select_related('usuario').get(pk=aluno.pk)
    )

    # Bloquear eixo durante a distribuição
    eixo = (
        Eixo.objects.select_for_update().select_related('edicao').get(pk=eixo_id, ativo=True, edicao__ativa=True)
    )

    if aluno.turno != Turno.NOTURNO:
        raise SorteioError('Esse sorteio é exclusivo do turno noturno.')

    if eixo.edicao.turno != Turno.NOTURNO:
        raise SorteioError('Esse eixo informado não pertence ao turno noturno')

    # Impedir que o santo sorteie novamente
    inscricao_existente = (
        InscricaoSorteio.objects.filter(aluno=aluno, edicao=eixo.edicao).select_related('eixo', 'grupo').first()
    )

    if inscricao_existente:
        return inscricao_existente, False

    grupos = list(
        Grupo.objects.filter(eixo=eixo).annotate(total_integrantes=Count('inscricoes'), mesmo_curso=Count('inscricoes', filter=Q(inscricoes__aluno__curso=aluno.curso)))
    )

    if len(grupos) != eixo.quantidade_grupos:
        raise SorteioConfiguracaoInvalida(' A quantidade de grupos cadastrados não corresponde as configurações do eixo ')

    grupos_com_vaga = [
        grupo for grupo in grupos 
        if grupo.total_integrantes < eixo.capacidade_grupo
    ]

    if not grupos_com_vaga:
        raise SorteioSemVagas('Não existem mais vagas neste eixo')

    # 1º critério: menor quantidade de alunos do mesmo curso
    menor_quantidade_mesmo_curso = min(
        grupo.mesmo_curso
        for grupo in grupos_com_vaga
    )

    candidatos = [
        grupo 
        for grupo in grupos_com_vaga
        if grupo.mesmo_curso == menor_quantidade_mesmo_curso
    ]

    # 2º critério: menor quantidade total de alunos
    menor_grupo = min(
        grupo.total_integrantes
        for grupo in candidatos
    )

    candidatos = [
        grupo 
        for grupo in candidatos
        if grupo.total_integrantes == menor_grupo
    ]

    # 3º critério: sorteio aleatório entre grupos equivalentes
    grupo_sorteado = secrets.choice(candidatos)

    inscricao = InscricaoSorteio.objects.create(
        aluno=aluno,
        edicao=eixo.edicao,
        eixo=eixo,
        grupo=grupo_sorteado
    )
    return inscricao, True

