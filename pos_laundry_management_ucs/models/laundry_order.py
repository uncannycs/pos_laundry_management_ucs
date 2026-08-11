# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class LaundryOrder(models.Model):
    _name = 'laundry.order'
    _description = 'Laundry Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now, required=True, tracking=True)
    expected_delivery_date = fields.Datetime(string='Expected Delivery Date', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Delivery'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)

    pos_order_id = fields.Many2one('pos.order', string='POS Order Reference', readonly=True, copy=False)
    session_id = fields.Many2one('pos.session', string='POS Session', readonly=True, copy=False)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    order_line_ids = fields.One2many('laundry.order.line', 'order_id', string='Order Lines', copy=True)
    
    amount_untaxed = fields.Monetary(string='Untaxed Amount', compute='_compute_amounts', store=True)
    amount_tax = fields.Monetary(string='Taxes', compute='_compute_amounts', store=True)
    amount_total = fields.Monetary(string='Total Amount', compute='_compute_amounts', store=True)

    is_urgent = fields.Boolean(string='Urgent / Express Service', default=False, tracking=True)
    urgent_charge = fields.Monetary(string='Urgent Fee', default=0.0)
    is_home_delivery = fields.Boolean(string='Home Delivery', default=False, tracking=True)
    delivery_charge = fields.Monetary(string='Delivery Fee', default=0.0)
    
    note = fields.Text(string='Special Instructions / Notes')
    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
    ], string='Payment Status', compute='_compute_payment_status', store=True)

    @api.depends('order_line_ids.price_subtotal', 'order_line_ids.price_total', 'is_urgent', 'urgent_charge', 'is_home_delivery', 'delivery_charge')
    def _compute_amounts(self):
        for order in self:
            untaxed = sum(line.price_subtotal for line in order.order_line_ids)
            total = sum(line.price_total for line in order.order_line_ids)
            tax = total - untaxed
            
            surcharges = 0.0
            if order.is_urgent:
                surcharges += order.urgent_charge
            if order.is_home_delivery:
                surcharges += order.delivery_charge

            order.amount_untaxed = untaxed
            order.amount_tax = tax
            order.amount_total = total + surcharges

    @api.depends('pos_order_id', 'pos_order_id.state')
    def _compute_payment_status(self):
        for order in self:
            if order.pos_order_id and order.pos_order_id.state in ('paid', 'done', 'invoiced'):
                order.payment_status = 'paid'
            elif order.state == 'delivered':
                order.payment_status = 'paid'
            else:
                order.payment_status = 'not_paid'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('laundry.order') or '/'
        return super().create(vals_list)

    def action_receive(self):
        for order in self:
            order.write({'state': 'received'})

    def action_process(self):
        for order in self:
            order.write({'state': 'processing'})

    def action_ready(self):
        for order in self:
            order.write({'state': 'ready'})

    def action_deliver(self):
        for order in self:
            order.write({'state': 'delivered'})

    def action_cancel(self):
        for order in self:
            order.write({'state': 'cancel'})

    def action_reset_draft(self):
        for order in self:
            order.write({'state': 'draft'})

    def action_view_pos_order(self):
        self.ensure_one()
        if not self.pos_order_id:
            raise UserError(_("No POS Order linked to this laundry order."))
        return {
            'name': _('POS Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'res_id': self.pos_order_id.id,
            'view_mode': 'form',
        }
