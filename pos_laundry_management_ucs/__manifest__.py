# -*- coding: utf-8 -*-
# Part of Uncanny Consulting Services LLP. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Laundry Management System UCS | POS Laundry Management | POS Dry Cleaning | Laundry Order Tracking | POS Laundry Receipt',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale/Laundry',
    'summary': 'Comprehensive POS Laundry Management System for Odoo 19 with full POS integration, service configuration, laundry workflow, urgent/delivery surcharges, and QWeb reports.',
    'description': """
        POS Laundry Management System UCS
        ==================================
        This module integrates complete laundry management operations natively with Odoo 19 Point of Sale (POS) and Backend ERP.

        Key Features:
        -------------
        * Full POS Integration: Configure laundry details (Expected delivery date, Urgent fee, Home delivery, Notes) directly in POS.
        * Service & Washing Types: Define service categories (Dry Clean, Wash & Fold, Iron Only, Starch, etc.) with custom surcharges.
        * Automated Laundry Order Creation: Generates backend Laundry Orders upon POS order validation.
        * Laundry Workflow Management: Draft -> Received -> Processing -> Ready -> Delivered -> Cancelled.
        * Garment-Level Notes & Services: Capture individual garment notes and washing preferences.
        * Smart POS Receipt: Displays laundry details, expected delivery date, and washing types on POS receipts.
        * Customer Integration & History: Smart button on customer forms to view complete laundry order history.
        * QWeb Printable Reports & Tags: Professional printable Laundry Work Ticket and Receipt reports.
        * Multi-Company Support: Full multi-company domain & security isolation.
    """,
    'author': 'Uncanny Consulting Services LLP',
    'company': 'Uncanny Consulting Services LLP',
    'website': 'https://uncannycs.com',
    'depends': ['point_of_sale', 'mail', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/laundry_sequence_data.xml',
        'data/laundry_data.xml',
        'wizard/laundry_order_cancel_wizard_views.xml',
        'views/laundry_washing_type_views.xml',
        'views/laundry_order_views.xml',
        'views/product_views.xml',
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'views/laundry_menus.xml',
        'report/laundry_order_report.xml',
        'report/laundry_order_report_template.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_laundry_management_ucs/static/src/scss/pos_laundry.scss',
            'pos_laundry_management_ucs/static/src/js/pos_laundry_model.js',
            'pos_laundry_management_ucs/static/src/js/pos_laundry_popup.js',
            'pos_laundry_management_ucs/static/src/js/pos_laundry_button.js',
            'pos_laundry_management_ucs/static/src/xml/pos_laundry_button.xml',
            'pos_laundry_management_ucs/static/src/xml/pos_laundry_popup.xml',
            'pos_laundry_management_ucs/static/src/xml/pos_laundry_receipt.xml',
        ],
    },
    'license': 'Other proprietary',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '100',
    'currency': 'USD',
    'images': ['static/description/banner.gif'],
}
