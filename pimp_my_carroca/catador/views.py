# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, redirect, flash, url_for,
                   current_app)
from flask.ext.login import login_required
from pimp_my_carroca.utils import flash_errors
from pimp_my_carroca.catador.forms import CatadorForm, BuscaCatadorRegiao
from pimp_my_carroca.catador.models import Catador
from geolocation.google_maps import GoogleMaps
from flask.ext.googlemaps import Map
from catadores_app import base


blueprint = Blueprint(
    "catador", __name__,
    url_prefix='/catador',
    static_folder="../static"
)


@blueprint.route('/inserir_base', methods=['GET'])
@login_required
def inserir_base():
    for catador in base:
        Catador(**catador).save()
    return redirect(url_for('catador.catadores_lista'))


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def catadores():
    form = CatadorForm()
    if form.validate_on_submit():
        novo_catador = Catador(
            nome=form.nome.data,
            telefone=form.telefone.data,
            endereco=form.endereco.data,
            latitude=form.latittude.data,
            longitude=form.longitude.data
        ).save()
        flash("O {} foi cadastrado com sucesso!".format(
            novo_catador.nome), 'success')
        return redirect(url_for('catador.catadores_lista'))
    else:
        flash_errors(form)
    return render_template('catadores/cadastro.html', form=form)


@blueprint.route('/listar', methods=['GET'])
@login_required
def catadores_lista():
    catadores = Catador.query.all()
    if not catadores:
        flash('Ainda não temos nenhum Catador cadastrado. =(', 'success')
    return render_template('catadores/lista.html', catadores=catadores)


@blueprint.route('/minha-regiao', methods=['GET', 'POST'])
@login_required
def catadores_regiao():
    form = BuscaCatadorRegiao()
    catadores = [(c.latitude, c.longitude) for c in Catador.query.all()]
    if form.validate_on_submit():
        google_maps = GoogleMaps(
            api_key=current_app.config['GOOGLEMAPS_API_KEY'])
        print(form.endereco.data)
        busca = google_maps.search(location=form.endereco.data)
        if not busca:
            flash('Não encontramos o endereço informado...', 'warnings')
            return render_template('catadores/mapa-regiao.html')

        busca_loc = busca.first()
        busca_lat = busca_loc.lat
        busca_lng = busca_loc.lng

        mapa = Map(
            identifier="view-side",
            lat=busca_lat,
            lng=busca_lng,
            markers=catadores,
            style="height:450px;width:450px;"
        )
        return render_template('catadores/mapa-regiao.html', mapa=mapa,
                               form=form)
    return render_template('catadores/mapa-regiao.html', form=form)
