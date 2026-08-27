from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from .models import Eixo, Grupo, Usuario, Aluno, Curso, Turno

class CadastroAlunoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=150)
    sobrenome = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    ra = serializers.CharField(max_length=10)
    data_nascimento = serializers.DateField()
    curso = serializers.ChoiceField(choices=Curso.choices)
    turno = serializers.ChoiceField(choices=Turno.choices)
    senha = serializers.CharField(write_only=True, trim_whitespace=False)
    confirmar_senha = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value):
        value = value.strip().lower()

        if Usuario.objects.filter(
            email__iexact=value
        ).exists():
            raise serializers.ValidationError('Já existe uma conta com esse e-mail')

        return value

    def validate_ra(self, value):
        value = value.strip().lower()

        if Aluno.objects.filter(ra=value).exists():
            raise serializers.ValidationError('Esse RA já está cadastrado')

        return value

    def validate(self, dados):
        if dados['senha'] != dados['confirmar_senha']:
            raise serializers.ValidationError({
                'confirmar_senha':
                'As senhas não coincidem.'
            })

        try:
            validate_password(dados['senha'])
        except DjangoValidationError as erro:
            raise serializers.ValidationError({
                'senha': list(erro.messages)
            })

        return dados

    @transaction.atomic
    def create(self, validated_data):
        senha = validated_data.pop('senha')

        validated_data.pop('confirmar_senha')

        usuario = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['nome'],
            last_name=validated_data['sobrenome'],
            password=senha
        )
        aluno = Aluno.objects.create(
            usuario=usuario,
            ra=validated_data['ra'],
            data_nascimento=validated_data['data_nascimento'],
            curso=validated_data['curso'],
            turno=validated_data['turno']
        )

        return aluno


class LoginSerializer(serializers.Serializer):
    ra = serializers.CharField(max_length=10)
    senha = serializers.CharField(write_only=True, trim_whitespace=False)


class EixoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eixo 
        fields = [
            'id',
            'nome_eixo',
            'ordem',
            'quantidade_grupos',
            'capacidade_grupo'
        ]

class IntegranteSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()

    class Meta:
        model = Aluno
        fields = [
            'nome',
            'curso'
        ]

    def get_nome(self, obj):
        return obj.usuario.get_full_name()

class GrupoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(read_only=True)
    integrantes = serializers.SerializerMethodField()

    class Meta:
        model = Grupo 
        fields = [
            'id',
            'nome',
            'numero',
            'integrantes'
        ]

    def get_integrantes(self, obj):
        alunos = [
            inscricao.aluno
            for inscricao in obj.inscricoes.all()
        ]
        return IntegranteSerializer(alunos, many=True).data

class SorteioSerializer(serializers.Serializer):
    eixo_id = serializers.IntegerField()