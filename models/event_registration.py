# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import logging

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.onchange('partner_id','event_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.event_id and self.event_id.event_type_id and self.event_id.event_type_id.miembro_ids:
            if self.partner_id.parent_id:
                cantidad_maxima = 0
                for linea_miembro in self.event_id.event_type_id.miembro_ids:
                    if linea_miembro.categoria_cliente == self.partner_id.parent_id.x_studio_catergoria_del_cliente_1:
                        cantidad_maxima = linea_miembro.cantidad

                if self.event_id.seats_expected == cantidad_maxima:
                    raise ValidationError(_("Error: El limite de participanstes es de: " +str(cantidad_maxima)))
