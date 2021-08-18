from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    diario_id = fields.Many2one('account.journal','Diario', domain="[('type', '=', 'sale')]")
