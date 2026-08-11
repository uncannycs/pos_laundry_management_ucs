# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class LaundryOrderLine(models.Model):
    _name = 'laundry.order.line'
    _description = 'Laundry Order Line'

    order_id = fields.Many2one('laundry.order', string='Laundry Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Laundry Item', required=True)
    washing_type_id = fields.Many2one('laundry.washing.type', string='Washing / Service Type')
    
    qty = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Monetary(string='Unit Price')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_line_amounts', store=True)
    price_total = fields.Monetary(string='Total', compute='_compute_line_amounts', store=True)
    
    note = fields.Char(string='Garment Notes', help='Specific garment instructions e.g., stain details, delicate fabric.')
    state = fields.Selection(related='order_id.state', store=True)
    company_id = fields.Many2one('res.company', related='order_id.company_id', store=True)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True)

    @api.depends('qty', 'price_unit', 'tax_ids')
    def _compute_line_amounts(self):
        for line in self:
            taxes = line.tax_ids.compute_all(
                line.price_unit,
                currency=line.currency_id,
                quantity=line.qty,
                product=line.product_id,
                partner=line.order_id.partner_id
            )
            line.price_subtotal = taxes['total_excluded']
            line.price_total = taxes['total_included']

    @api.onchange('product_id', 'washing_type_id')
    def _onchange_product_or_washing_type(self):
        if not self.product_id:
            return
        base_price = self.product_id.lst_price
        if hasattr(self.product_id, 'laundry_charge') and self.product_id.laundry_charge:
            base_price = self.product_id.laundry_charge
        
        extra = 0.0
        if self.washing_type_id:
            extra = self.washing_type_id.extra_charge
            
        self.price_unit = base_price + extra
        if not self.tax_ids:
            self.tax_ids = self.product_id.taxes_id
