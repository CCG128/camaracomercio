# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Event(models.Model):
    _inherit = 'event.event'

    compra_subtotal = fields.Monetary(
        string='Compras (Impuestos excluidos)', compute='_compute_compra_subtotal_margenes')
    utilidad = fields.Monetary('Utilidad', compute='_compute_compra_subtotal_margenes',store=True)
    margen = fields.Float('Margen', compute='_compute_compra_subtotal_margenes', store=True)

    def _compute_compra_subtotal_margenes(self):
        for evento in self:
            compra_subtotal_evento = 0
            utilidad = 0
            margen = 0
            compra_ids = self.env['purchase.order'].search([('evento_id','=',evento.id),('state','=','purchase')])
            if compra_ids:
                for compra in compra_ids:
                    compra_subtotal_evento += compra.amount_untaxed
            utilidad = evento.sale_price_subtotal-compra_subtotal_evento
            if evento.sale_price_subtotal > 0:
                margen = (evento.sale_price_subtotal-compra_subtotal_evento) / evento.sale_price_subtotal
            evento.utilidad = utilidad
            evento.margen = margen * 100
            evento.compra_subtotal = compra_subtotal_evento

class EventType(models.Model):
    _inherit = 'event.type'

    miembros = fields.Boolean('Acompañante miembros')
    miembro_ids = fields.One2many('camaracomercio.config.miembros','tipo_evento_id','Miembros')
