# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import time
import base64
import io
import logging
import xlsxwriter

class camaracomercio_reporte_cobros_wizard(models.TransientModel):
    _name = 'camaracomercio.reporte_cobros.wizard'

    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    archivo = fields.Binary('Archivo')
    name =  fields.Char('File Name', size=32)


    def print_report_excel(self):
        datos = ''
        for w in self:
            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f)
            hoja = libro.add_worksheet('Reporte')
            pago_ids = self.env['account.payment'].search([('partner_type','=','customer'),('date','>=', w.fecha_inicio),('date','<=', w.fecha_fin)])

            hoja.write(0, 0, 'REPORTE DE COBROS')
            hoja.write(0, 1, 'Fecha inicio')
            hoja.write(0, 2, str(w.fecha_inicio))
            hoja.write(0, 3, 'Fecha fin')
            hoja.write(0, 4, str(w.fecha_fin))

            hoja.write(2, 0, 'Código cliente')
            hoja.write(2, 1, 'Cliente')
            hoja.write(2, 2, 'Fecha de pago')
            hoja.write(2, 3, 'Factura / Recibo')
            hoja.write(2, 4, 'Vendedor')
            hoja.write(2, 5, 'Cobrador')
            hoja.write(2, 6, 'Recibo de Caja')
            hoja.write(2, 7, 'Documento')
            hoja.write(2, 8, 'Fecha de factura')
            hoja.write(2, 9, 'Total')
            fila = 3
            if pago_ids:
                for pago in pago_ids:
                    if pago.reconciled_invoice_ids:
                        for factura in  pago.reconciled_invoice_ids:
                            hoja.write(fila, 0, factura.partner_id.id)
                            hoja.write(fila, 1, factura.partner_id.name)
                            hoja.write(fila, 2, str(pago.date))
                            hoja.write(fila, 3, factura.journal_id.tipo_documento_fel)
                            hoja.write(fila, 4, factura.invoice_user_id.name)
                            hoja.write(fila, 5, factura.cobrador_id.name if factura.cobrador_id else '')
                            hoja.write(fila, 6, pago.x_studio_no_de_recibo)
                            hoja.write(fila, 7, factura.ref)
                            hoja.write(fila, 8, factura.invoice_date)
                            hoja.write(fila, 9, pago.amount)
                            fila += 1

            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'reporte_cobros.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'camaracomercio.reporte_cobros.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
