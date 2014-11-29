#! -*- coding: utf-8 -*-

from pimp_my_carroca.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Catador(SurrogatePK, Model):

    __tablename__ = 'catador'
    nome = Column(db.String(80), nullable=False)
    telefone = Column(db.String(25))
    endereco = Column(db.String(255))
    latitude = Column(db.Integer, nullable=False)
    longitude = Column(db.Integer, nullable=False)
