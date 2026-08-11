# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        models_list = super()._load_pos_data_models(config_id)
        if 'laundry.washing.type' not in models_list:
            models_list.append('laundry.washing.type')
        return models_list


class PosOrder(models.Model):
    _inherit = 'pos.order'

    laundry_order_id = fields.Many2one('laundry.order', string='Laundry Order', copy=False)
    is_laundry_order = fields.Boolean(string='Is Laundry Order', copy=False)
    laundry_status = fields.Selection(related='laundry_order_id.state', string='Laundry Status', store=True)
    expected_delivery_date = fields.Datetime(string='Expected Delivery Date')
    laundry_note = fields.Text(string='Laundry Note')
    is_urgent = fields.Boolean(string='Urgent Service')
    is_home_delivery = fields.Boolean(string='Home Delivery')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super()._order_fields(ui_order)
        order_fields['is_laundry_order'] = ui_order.get('is_laundry_order', False)
        date_val = ui_order.get('expected_delivery_date')
        if date_val and isinstance(date_val, str):
            date_val = date_val.replace('T', ' ')
            if len(date_val) == 16:
                date_val += ':00'
        order_fields['expected_delivery_date'] = date_val if date_val else False
        order_fields['laundry_note'] = ui_order.get('laundry_note') or ''
        order_fields['is_urgent'] = ui_order.get('is_urgent', False)
        order_fields['is_home_delivery'] = ui_order.get('is_home_delivery', False)
        return order_fields

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            date_val = vals.get('expected_delivery_date')
            if date_val and isinstance(date_val, str):
                date_val = date_val.replace('T', ' ')
                if len(date_val) == 16:
                    date_val += ':00'
                vals['expected_delivery_date'] = date_val
        orders = super().create(vals_list)
        for order in orders:
            if order.is_laundry_order or any(line.product_id.is_laundry_product or line.washing_type_id for line in order.lines):
                order._create_laundry_order()
        return orders

    def _create_laundry_order(self):
        for order in self:
            if order.laundry_order_id:
                continue
            laundry_lines = []
            for line in order.lines:
                laundry_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'washing_type_id': line.washing_type_id.id if line.washing_type_id else False,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'tax_ids': [(6, 0, line.tax_ids.ids)],
                    'note': line.laundry_item_note or '',
                }))

            partner_id = order.partner_id.id if order.partner_id else self.env.ref('base.public_partner').id
            urgent_fee = order.config_id.default_urgent_fee if order.is_urgent else 0.0
            delivery_fee = order.config_id.default_delivery_fee if order.is_home_delivery else 0.0

            laundry_order = self.env['laundry.order'].create({
                'partner_id': partner_id,
                'order_date': order.date_order,
                'expected_delivery_date': order.expected_delivery_date,
                'pos_order_id': order.id,
                'session_id': order.session_id.id,
                'user_id': order.user_id.id,
                'company_id': order.company_id.id,
                'currency_id': order.currency_id.id,
                'is_urgent': order.is_urgent,
                'urgent_charge': urgent_fee,
                'is_home_delivery': order.is_home_delivery,
                'delivery_charge': delivery_fee,
                'note': order.laundry_note,
                'state': 'received',
                'order_line_ids': laundry_lines,
            })
            order.laundry_order_id = laundry_order.id

    def action_view_laundry_order(self):
        self.ensure_one()
        if not self.laundry_order_id:
            raise models.UserError(_("No Laundry Order linked to this POS Order."))
        return {
            'name': _('Laundry Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'laundry.order',
            'res_id': self.laundry_order_id.id,
            'view_mode': 'form',
        }


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    washing_type_id = fields.Many2one('laundry.washing.type', string='Washing Type')
    laundry_item_note = fields.Char(string='Garment Note')

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        res = list(params) if params else []
        for field in ['washing_type_id', 'laundry_item_note']:
            if field not in res:
                res.append(field)
        return res

    @api.model
    def _order_line_fields(self, line, session_id=None):
        res = super()._order_line_fields(line, session_id)
        if len(line) >= 3 and isinstance(line[2], dict):
            wt = line[2].get('washing_type_id', False)
            if isinstance(wt, dict):
                wt = wt.get('id', False)
            res[2]['washing_type_id'] = wt if wt else False
            res[2]['laundry_item_note'] = line[2].get('laundry_item_note') or ''
        return res
