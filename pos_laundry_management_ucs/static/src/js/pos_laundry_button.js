import { _t } from "@web/core/l10n/translation";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { LaundryOrderPopup, LaundryLinePopup } from "./pos_laundry_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ControlButtons.prototype, {
    async clickLaundryDetails() {
        const order = this.pos.get_order();
        if (!order) return;

        const payload = await makeAwaitable(this.dialog, LaundryOrderPopup, {
            order: order,
        });

        if (payload) {
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
    },

    async clickWashingType() {
        const order = this.pos.get_order();
        const selectedLine = order?.get_selected_orderline();
        if (!selectedLine) {
            this.dialog.add(AlertDialog, {
                title: _t("No Line Selected"),
                body: _t("Please select an order line first to assign a washing service or garment note."),
            });
            return;
        }

        const washingTypes = this.pos.models["laundry.washing.type"] 
            ? this.pos.models["laundry.washing.type"].getAll() 
            : [];

        const payload = await makeAwaitable(this.dialog, LaundryLinePopup, {
            line: selectedLine,
            washingTypes: washingTypes,
        });

        if (payload) {
            selectedLine.washing_type_id = payload.washing_type_id;
            selectedLine.laundry_item_note = payload.laundry_item_note;

            if (payload.washing_type_id && payload.washing_type_id.extra_charge > 0) {
                const basePrice = selectedLine.product_id.laundry_charge || selectedLine.product_id.lst_price || selectedLine.price_unit;
                selectedLine.set_unit_price(basePrice + payload.washing_type_id.extra_charge);
            }
        }
    },
});
