# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    ticket_padre_id = fields.Many2one('helpdesk.ticket','Ticket padre')
