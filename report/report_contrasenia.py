# -*- coding: utf-8 -*-

from odoo import api, models
import re
import odoo.addons.l10n_gt_extra.a_letras
import logging
from datetime import date
import datetime

class ReportContrasenia(models.AbstractModel):
    _name = 'report.camaracomercio.reporte_contrasenia'

    nombre_reporte = ''

    def movimientos(self,o):
        datos = []
        totales = []
        movimientos = self.env['account.move.line'].search([
            ('move_id', '=', o.id)])
        debit = 0
        credit = 0
        for i in movimientos:
            debit += i.debit
            credit += i.credit
            datos.append({
                'code':i.account_id.code,
                'name':i.account_id.name,
                'analitica':i.analytic_account_id.name,
                'debit': i.debit,
                'credit': i.credit,
                })
        totales.append({
            'debit': debit,
            'credit': credit,
            })
        return {'datos': datos, 'totales':totales}

    def fecha_actual(self):
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%Y/%m/%d %H:%M:%S %p')
        return hoy

    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'account.move'
        docs = self.env['account.move'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'movimientos': self.movimientos,
            'fecha_actual': self.fecha_actual,
            'a_letras': odoo.addons.l10n_gt_extra.a_letras,
        }

class ReportFacturaElectronica(models.AbstractModel):
    _name = 'report.camaracomercio.report_factura_electronica'
    _inherit = 'report.camaracomercio.reporte_contrasenia'
