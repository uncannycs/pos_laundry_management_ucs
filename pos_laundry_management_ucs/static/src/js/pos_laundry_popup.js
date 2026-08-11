/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";

export class LaundryOrderPopup extends AbstractAwaitablePopup {
    static template = "pos_laundry_management_ucs.LaundryOrderPopup";
    static defaultProps = {
        title: _t("Laundry Order Options"),
        order: null,
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({
            expected_delivery_date: this.props.order ? (this.props.order.expected_delivery_date || "") : "",
            laundry_note: this.props.order ? (this.props.order.laundry_note || "") : "",
            is_urgent: this.props.order ? (this.props.order.is_urgent || false) : false,
            is_home_delivery: this.props.order ? (this.props.order.is_home_delivery || false) : false,
        });
    }

    getPayload() {
        return {
            expected_delivery_date: this.state.expected_delivery_date,
            laundry_note: this.state.laundry_note,
            is_urgent: this.state.is_urgent,
            is_home_delivery: this.state.is_home_delivery,
        };
    }
}

export class LaundryLinePopup extends AbstractAwaitablePopup {
    static template = "pos_laundry_management_ucs.LaundryLinePopup";
    static defaultProps = {
        title: _t("Garment Service & Notes"),
        line: null,
        washingTypes: [],
    };

    setup() {
        super.setup();
        this.pos = usePos();
        const initialType = (this.props.line && this.props.line.washing_type_id) 
            ? (this.props.line.washing_type_id.id || this.props.line.washing_type_id) 
            : "";
        this.state = useState({
            washing_type_id: initialType,
            laundry_item_note: this.props.line ? (this.props.line.laundry_item_note || "") : "",
        });
    }

    getPayload() {
        const selectedType = this.props.washingTypes.find(
            (t) => t.id === parseInt(this.state.washing_type_id)
        ) || false;
        return {
            washing_type_id: selectedType,
            laundry_item_note: this.state.laundry_item_note,
        };
    }
}
