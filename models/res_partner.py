# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class ResPartner(models.Model):
    _inherit = "res.partner"

    estado = fields.Selection([ ('no_afiliado', 'No afiliado'),
        ('afiliado_activo', 'Afiliado / Activo'),
        ('afiliado_moroso', 'Afiliado / Moroso'),
        ('afiliado_retirar', 'Afiliado / Por retirar')],'Estado', default='no_afiliado')

    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado:
            estado_ids = self.env['camaracomercio.config.estado'].search([('estado','=',self.estado)])
            if estado_ids:
                self.property_product_pricelist = estado_ids[0].tarifa_id.id
