# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class LaundryWashingType(models.Model):
    _name = 'laundry.washing.type'
    _description = 'Laundry Service / Washing Type'

    name = fields.Char(string='Service Name', required=True, translate=True)
    code = fields.Char(string='Code')
    extra_charge = fields.Monetary(string='Extra Charge', default=0.0, help='Extra surcharge for this specific washing service.')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
