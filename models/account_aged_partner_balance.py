# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
import logging

class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner"

    def _get_column_details(self, options):
        res = super(ReportAccountAgedPartner, self)._get_column_details(options)
        res[1] = self._field_column('report_date', name='Fecha de factura')
        res[4] = self._field_column('expected_pay_date', name='Fecha de vencimiento')
        return res

    def _show_line(self, report_dict, value_dict, current, options):
        if 'name' in report_dict and 'parent_id' in report_dict:
            if report_dict['parent_id'] != None:
                factura = self.env['account.move'].search([('name', '=', report_dict['name'])])
                if factura.serie_fel:
                    report_dict['name'] = report_dict['name'] + ' - ' + factura.serie_fel
                if factura.numero_fel:
                    report_dict['name'] = report_dict['name'] + ' - ' + factura.numero_fel

        return super(ReportAccountAgedPartner, self)._show_line(report_dict, value_dict, current, options)
