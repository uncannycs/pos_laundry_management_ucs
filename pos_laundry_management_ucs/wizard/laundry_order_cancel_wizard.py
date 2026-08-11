# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class LaundryOrderCancelWizard(models.TransientModel):
    _name = 'laundry.order.cancel.wizard'
    _description = 'Laundry Order Cancel Wizard'

    order_id = fields.Many2one('laundry.order', string='Laundry Order', required=True, default=lambda self: self.env.context.get('active_id'))
    cancel_reason = fields.Text(string='Reason for Cancellation', required=True)

    def action_confirm_cancel(self):
        self.ensure_one()
        self.order_id.write({
            'state': 'cancel',
            'note': (self.order_id.note or '') + f"\n[Cancellation Reason]: {self.cancel_reason}"
        })
        self.order_id.message_post(body=_("Order cancelled. Reason: %s") % self.cancel_reason)
        return {'type': 'ir.actions.act_window_close'}
