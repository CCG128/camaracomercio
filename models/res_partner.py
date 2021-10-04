# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class ResPartner(models.Model):
    _inherit = "res.partner"

    estado = fields.Selection([ ('no_afiliado', 'No afiliado'),
        ('afiliado_activo', 'Afiliado / Activo'),
        ('afiliado_moroso', 'Afiliado / Moroso'),
        ('afiliado_retirar', 'Afiliado / Por retirar')],'Estado', default='no_afiliado')
