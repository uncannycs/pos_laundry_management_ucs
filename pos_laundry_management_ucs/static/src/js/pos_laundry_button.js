/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { LaundryOrderPopup, LaundryLinePopup } from "./pos_laundry_popup";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class LaundryDetailsButton extends Component {
    static template = "pos_laundry_management_ucs.LaundryDetailsButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    get currentOrder() {
        return this.pos.get_order();
    }

    async onClick() {
        const order = this.pos.get_order();
        if (!order) return;

        const { confirmed, payload } = await this.popup.add(LaundryOrderPopup, {
            order: order,
        });

        if (confirmed && payload) {
            order.is_laundry_order = true;
            let formattedDate = payload.expected_delivery_date ? payload.expected_delivery_date.replace("T", " ") : false;
            if (formattedDate && formattedDate.length === 16) {
                formattedDate += ":00";
            }
            order.expected_delivery_date = formattedDate;
            order.laundry_note = payload.laundry_note;
            order.is_urgent = payload.is_urgent;
            order.is_home_delivery = payload.is_home_delivery;
        }
    }
}

ProductScreen.addControlButton({
    component: LaundryDetailsButton,
    condition: function () {
        return this.pos.config && this.pos.config.enable_laundry;
    },
});

export class GarmentServiceButton extends Component {
    static template = "pos_laundry_management_ucs.GarmentServiceButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    async onClick() {
        const order = this.pos.get_order();
        const selectedLine = order?.get_selected_orderline();
        if (!selectedLine) {
            this.popup.add(ErrorPopup, {
                title: _t("No Line Selected"),
                body: _t("Please select an order line first to assign a washing service or garment note."),
            });
            return;
        }

        const washingTypes = this.pos.laundry_washing_type 
            || (this.pos.models && this.pos.models["laundry.washing.type"] ? this.pos.models["laundry.washing.type"].getAll() : []) 
            || [];

        const { confirmed, payload } = await this.popup.add(LaundryLinePopup, {
            line: selectedLine,
            washingTypes: washingTypes,
        });

        if (confirmed && payload) {
            selectedLine.washing_type_id = payload.washing_type_id;
            selectedLine.laundry_item_note = payload.laundry_item_note;

            const product = selectedLine.get_product();
            const basePrice = product.laundry_charge || product.lst_price || selectedLine.get_unit_price();

            if (payload.washing_type_id && payload.washing_type_id.extra_charge > 0) {
                selectedLine.set_unit_price(basePrice + payload.washing_type_id.extra_charge);
            } else {
                selectedLine.set_unit_price(basePrice);
            }
        }
    }
}

ProductScreen.addControlButton({
    component: GarmentServiceButton,
    condition: function () {
        return this.pos.config && this.pos.config.enable_laundry;
    },
});
