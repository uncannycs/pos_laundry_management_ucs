# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_laundry_product = fields.Boolean(string='Is Laundry Product', default=False, help='Check if this product is a garment or item processed by the laundry system.')
    laundry_washing_type_ids = fields.Many2many('laundry.washing.type', string='Allowed Washing Types')
    laundry_charge = fields.Monetary(string='Base Laundry Charge', help='Default base pricing for laundry service of this product.')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        res = list(params) if params else []
        for field in ['is_laundry_product', 'laundry_washing_type_ids', 'laundry_charge']:
            if field not in res:
                res.append(field)
        return res
