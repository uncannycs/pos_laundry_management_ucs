# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_laundry = fields.Boolean(string='Enable Laundry Management', default=True, help='Enable POS Laundry Order functionality for this Point of Sale.')
    default_delivery_fee = fields.Float(string='Default Home Delivery Fee', default=10.0)
    default_urgent_fee = fields.Float(string='Default Urgent Service Fee', default=15.0)
