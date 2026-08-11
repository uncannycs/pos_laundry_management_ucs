# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_laundry_product = fields.Boolean(string='Is Laundry Product', default=False, help='Check if this product is a garment or item processed by the laundry system.')
    laundry_washing_type_ids = fields.Many2many('laundry.washing.type', string='Allowed Washing Types')
    laundry_charge = fields.Monetary(string='Base Laundry Charge', help='Default base pricing for laundry service of this product.')
