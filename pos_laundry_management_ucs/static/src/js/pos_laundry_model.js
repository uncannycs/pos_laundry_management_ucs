/** @odoo-module **/

import { Order, Orderline } from "@point_of_sale/app/store/models";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.laundry_washing_type = loadedData["laundry.washing.type"] || [];
    },
});

patch(Order.prototype, {
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        let formattedDate = this.expected_delivery_date ? this.expected_delivery_date.replace("T", " ") : false;
        if (formattedDate && formattedDate.length === 16) {
            formattedDate += ":00";
        }
        json.is_laundry_order = this.is_laundry_order || false;
        json.expected_delivery_date = formattedDate;
        json.laundry_note = this.laundry_note || "";
        json.is_urgent = this.is_urgent || false;
        json.is_home_delivery = this.is_home_delivery || false;
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.is_laundry_order = json.is_laundry_order || false;
        this.expected_delivery_date = json.expected_delivery_date || false;
        this.laundry_note = json.laundry_note || "";
        this.is_urgent = json.is_urgent || false;
        this.is_home_delivery = json.is_home_delivery || false;
    },
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.is_laundry_order = this.is_laundry_order;
        result.expected_delivery_date = this.expected_delivery_date;
        result.laundry_note = this.laundry_note;
        result.is_urgent = this.is_urgent;
        result.is_home_delivery = this.is_home_delivery;
        return result;
    },
});

patch(Orderline.prototype, {
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.washing_type_id = this.washing_type_id ? (this.washing_type_id.id || this.washing_type_id) : false;
        json.laundry_item_note = this.laundry_item_note || "";
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.washing_type_id = json.washing_type_id || false;
        this.laundry_item_note = json.laundry_item_note || "";
    },
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.washing_type_id = this.washing_type_id;
        result.washing_type_name = this.washing_type_id ? (this.washing_type_id.name || "") : "";
        result.laundry_item_note = this.laundry_item_note;
        return result;
    },
});
