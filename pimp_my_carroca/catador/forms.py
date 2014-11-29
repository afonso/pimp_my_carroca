#! -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

from .models import Catador


class CatadorForm(Form):
    nome = TextField(
        'Nome: ', validators=[DataRequired(), Length(min=3, max=25)])
    telefone = TextField('Telefone: ')
    endereco = TextField('Endereço: ')
    latittude = IntegerField('Latitude: ')
    longitude = IntegerField('Longitude: ')

    cadastrar = SubmitField('Cadastrar')

    def validate(self):
        initial_validation = super(CatadorForm, self).validate()
        if not initial_validation:
            return False
        catador = Catador.query.filter_by(
            nome=self.nome.data,
            telefone=self.telefone.data,
            endereco=self.endereco.data
        ).first()
        if catador:
            self.nome.errors.append("O {} está cadastrado no sistema!".format(
                self.nome.data))
            return False
        return True


class BuscaCatadorRegiao(Form):
    endereco = TextField('Endereço: ')
    buscar = SubmitField('Buscar Catador!')
