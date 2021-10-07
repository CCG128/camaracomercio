# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

class CamaraomercioConfigEstado(models.Model):
    _name = "camaracomercio.config.estado"

    estado = fields.Selection([ ('no_afiliado', 'No afiliado'),
        ('afiliado_activo', 'Afiliado / Activo'),
        ('afiliado_moroso', 'Afiliado / Moroso'),
        ('afiliado_retirar', 'Afiliado / Por retirar')],'Estado', default='no_afiliado')
    tarifa_id = fields.Many2one('product.pricelist','Tarifa')
    dias = fields.Integer('Días')
    bloquear_cliente = fields.Boolean('Bloquear cliente')


class CamaraomercioConfgMiembros(models.Model):
    _name = "camaracomercio.config.miembros"

    tipo_evento_id = fields.Many2one('event.type','Tipo de evento')
    categoria_cliente = fields.Selection([ ('Afiliado Tipo Departamental', 'Afiliado Tipo Departamental'),
        ('Afiliado Tipo A', 'Afiliado Tipo A'),
        ('Afiliado Tipo AA', 'Afiliado Tipo AA'),
        ('Afiliado Tipo B', 'Afiliado Tipo B'),
        ('Afiliado Tipo C', 'Afiliado Tipo C'),
        ('Afiliado Tipo D', 'Afiliado Tipo D'),
        ('Afiliado TIpo E', 'Afiliado TIpo E'),
        ('Círculo de Mujeres', 'Círculo de Mujeres'),
        ('No Afiliado', 'No Afiliado')],'Categoría del cliente')
    cantidad = fields.Integer('Cantidad')
