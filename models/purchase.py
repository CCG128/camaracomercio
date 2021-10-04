# -*- coding: utf-8 -*-

from odoo import api, fields, models, _



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    evento_id = fields.Many2one('event.event','Evento')
