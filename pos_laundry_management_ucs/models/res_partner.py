# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    laundry_order_count = fields.Integer(compute='_compute_laundry_order_count', string='Laundry Orders Count')

    def _compute_laundry_order_count(self):
        for partner in self:
            partner.laundry_order_count = self.env['laundry.order'].search_count([('partner_id', '=', partner.id)])

    def action_view_laundry_orders(self):
        self.ensure_one()
        return {
            'name': _('Laundry Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'laundry.order',
            'view_mode': 'kanban,list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
