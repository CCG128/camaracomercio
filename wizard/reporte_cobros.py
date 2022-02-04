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
            hoja.write(2, 3, 'Cobrador')
            hoja.write(2, 4, 'Recibo de Caja')
            hoja.write(2, 5, 'Total pago')
            hoja.write(2, 6, 'Fecha factura')
            hoja.write(2, 7, 'Factura / Recibo')
            hoja.write(2, 8, 'Vendedor')
            hoja.write(2, 9, 'Documento')
            hoja.write(2, 10, 'Total Factura')
            hoja.write(2, 11, 'Producto')
            hoja.write(2, 12, 'Cuenta Analítica')
            hoja.write(2, 13, 'Valor linea')

            fila = 3
            pagos = {}
            if pago_ids:
                for pago in pago_ids:
                    if pago.reconciled_invoice_ids:
                        if pago.id not in pagos:
                            id_linea = pago.reconciled_invoice_ids[0].invoice_line_ids[0].id
                            linea = pago.reconciled_invoice_ids[0].invoice_line_ids[0]
                            factura_recibo = pago.reconciled_invoice_ids[0].journal_id.tipo_documento_fel
                            factura_primera_linea_id = pago.reconciled_invoice_ids[0].id
                            pagos[pago.id] = {
                                'pago_id': pago,
                                'codigo_cliente': pago.partner_id.id,
                                'cliente': pago.partner_id.name,
                                'fecha_pago': str(pago.date),
                                'primera_linea': {'id': id_linea, 'linea': linea},
                                'lineas_factura': [],
                                'recibo_caja': pago.x_studio_no_de_recibo,
                                'total_pago': pago.amount,
                                'facturas_primera_linea': [factura_primera_linea_id],
                                 }

                        for factura in pago.reconciled_invoice_ids:
                            for linea in factura.invoice_line_ids:
                                if linea.id != pagos[pago.id]['primera_linea']['id']:
                                    pagos[pago.id]['lineas_factura'].append(linea)

                fila = 3
                if pagos:
                    for pago in pagos:
                        hoja.write(fila,0,pagos[pago]['pago_id'].partner_id.id)
                        hoja.write(fila,1,pagos[pago]['pago_id'].partner_id.name)
                        hoja.write(fila,2,str(pagos[pago]['pago_id'].date))
                        if pagos[pago]['primera_linea']:
                            hoja.write(fila,3,pagos[pago]['primera_linea']['linea'].move_id.cobrador_id.name if pagos[pago]['primera_linea']['linea'].move_id.cobrador_id else "" )
                            hoja.write(fila,10,pagos[pago]['primera_linea']['linea'].move_id.amount_total)
                            hoja.write(fila,11,pagos[pago]['primera_linea']['linea'].name)
                            hoja.write(fila,12,pagos[pago]['primera_linea']['linea'].analytic_account_id.name if pagos[pago]['primera_linea']['linea'].analytic_account_id else "")
                            hoja.write(fila,13,pagos[pago]['primera_linea']['linea'].price_total)

                        hoja.write(fila,4, pagos[pago]['pago_id'].x_studio_no_de_recibo)
                        hoja.write(fila,5, pagos[pago]['pago_id'].amount)
                        hoja.write(fila,6, str(pagos[pago]['primera_linea']['linea'].move_id.invoice_date))
                        hoja.write(fila,7, pagos[pago]['primera_linea']['linea'].move_id.journal_id.tipo_documento_fel)
                        hoja.write(fila,8, pagos[pago]['primera_linea']['linea'].move_id.invoice_user_id.name)
                        hoja.write(fila,9, pagos[pago]['primera_linea']['linea'].move_id.ref)


                        # Recorremos lineas_factura para desplegar las lines restantes de las facturas
                        fila += 1
                        if pagos[pago]['lineas_factura']:
                            for lf in pagos[pago]['lineas_factura']:
                                hoja.write(fila, 0, pagos[pago]['pago_id'].partner_id.id)
                                hoja.write(fila, 1, pagos[pago]['pago_id'].partner_id.name)
                                hoja.write(fila, 2, str(pagos[pago]['pago_id'].date))
                                hoja.write(fila, 3, lf.move_id.cobrador_id.name if lf.move_id.cobrador_id else "")
                                hoja.write(fila, 4, pagos[pago]['pago_id'].x_studio_no_de_recibo)
                                hoja.write(fila, 6, str(lf.move_id.invoice_date))
                                hoja.write(fila, 7, lf.move_id.journal_id.tipo_documento_fel)
                                hoja.write(fila, 8, lf.move_id.invoice_user_id.name)
                                hoja.write(fila, 9, lf.move_id.ref)

                                # Si la factura no existe en facturas_primera_linea, la agregamos y desplegamos el total de la factura en fila, 10
                                if lf.move_id.id not in pagos[pago]['facturas_primera_linea']:
                                    pagos[pago]['facturas_primera_linea'].append(lf.move_id.id)
                                    hoja.write(fila,10, lf.move_id.amount_total)

                                hoja.write(fila,11,lf.name)
                                hoja.write(fila,12,lf.analytic_account_id.name if lf.analytic_account_id else "")
                                hoja.write(fila,13, lf.price_total)
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
