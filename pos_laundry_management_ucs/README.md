# POS Laundry Management System UCS

**Technical Name:** `pos_laundry_management_ucs`  
**Odoo Version:** 18.0  
**Author:** Uncanny Consulting Services LLP  
**Website:** https://uncannycs.com  

---

## Overview
The **POS Laundry Management System UCS** module extends Odoo 18 Point of Sale (POS) and Backend ERP to provide a complete end-to-end laundry management system.

### Key Features
1. **POS Integration**:
   - Capture expected delivery date & time.
   - Apply Express / Urgent service surcharges.
   - Apply Home Delivery charges.
   - Add general laundry notes and item-level garment instructions.
   - Select washing / service types (Dry Cleaning, Wash & Fold, Ironing, Starch, etc.).
   - Print POS Receipts with full laundry details.

2. **Backend Laundry Management**:
   - Complete status workflow: **Draft -> Received -> Processing -> Ready -> Delivered -> Cancelled**.
   - Manage washing service types and surcharges.
   - Track customer history with dedicated Laundry smart buttons.
   - Multi-company security & domain isolation.
   - QWeb printable Laundry Work Tickets & Customer Receipts.

---

## Installation & Configuration
1. Place `pos_laundry_management_ucs` in your custom addons directory.
2. Update App List in Odoo 18 (`Apps -> Update Apps List`).
3. Install **POS Laundry Management System UCS**.
4. Configure Washing Types under **Point of Sale -> Laundry Management -> Washing Types**.
5. Enable Laundry Management in **Point of Sale -> Configuration -> Settings**.
