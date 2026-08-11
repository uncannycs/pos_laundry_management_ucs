# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_enable_laundry = fields.Boolean(
        related='pos_config_id.enable_laundry',
        readonly=False,
        string='Enable Laundry Management'
    )
    pos_default_delivery_fee = fields.Float(
        related='pos_config_id.default_delivery_fee',
        readonly=False,
        string='Default Delivery Fee'
    )
    pos_default_urgent_fee = fields.Float(
        related='pos_config_id.default_urgent_fee',
        readonly=False,
        string='Default Urgent Fee'
    )
