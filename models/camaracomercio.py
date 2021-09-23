# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

class CamaraomercioConfigEstado(models.Model):
    _name = "camaracomercio.config.estado"

    estado = fields.Selection([ ('no_afiliado', 'No afiliado'),
        ('afiliado', 'Afiliado'),
        ('afiliado_activo', 'Afiliado / Activo'),
        ('afiliado_moroso', 'Afiliado / Moroso'),
        ('afiliado_retirar', 'Afiliado / Por retirar')],'Estado', default='no_afiliado')
    tarifa_id = fields.Many2one('product.pricelist','Tarifa')
    dias = fields.Integer('Días')
    bloquear_cliente = fields.Boolean('Bloquear cliente')
