# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.move_type in ["out_invoice","out_refund"] and self.invoice_line_ids:
            if self.partner_id.property_product_pricelist and self.amount_residual > 0:
                self.verificar_estado_cliente(self.partner_id.property_product_pricelist, self.invoice_date)
            self.verificar_productos_diferentes(self.journal_id,self.invoice_line_ids)
        return res

    def verificar_productos_diferentes(self,journal_id,invoice_line_ids):
        productos_diferentes = []
        for linea in invoice_line_ids:
            if linea.product_id.product_tmpl_id.diario_id.id != journal_id.id:
                productos_diferentes.append(linea.product_id.name)
        if len(productos_diferentes) > 0:
            raise UserError(_('El diario de los siguientes productos '+ str(productos_diferentes) +' debe de ser el mismo que el de la factura'))
        else:
            return True

    def verificar_estado_cliente(self,tarifa_id, fecha_factura):
        dias_retraso = 0
        tarifa_ids = self.env['camaracomercio.config.estado'].search([('tarifa_id','=',tarifa_id.id),('bloquear_cliente','=',True)])
        fecha_hoy = fields.Date.today()
        dias_retraso = (fecha_hoy - fecha_factura).days + 1
        if tarifa_ids:
            for tarifa in tarifa_ids:
                if dias_retraso >= tarifa.dias:
                    raise UserError(_('Usuario bloqueado dias de retraso permitidos '+ str(tarifa.dias)))
        return True
