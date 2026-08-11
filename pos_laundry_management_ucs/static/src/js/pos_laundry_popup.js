import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";

export class LaundryOrderPopup extends Component {
    static components = { Dialog };
    static template = "pos_laundry_management_ucs.LaundryOrderPopup";
    static props = {
        close: Function,
        getPayload: Function,
        order: Object,
    };

    setup() {
        this.pos = usePos();
        this.state = useState({
            expected_delivery_date: this.props.order.expected_delivery_date || "",
            laundry_note: this.props.order.laundry_note || "",
            is_urgent: this.props.order.is_urgent || false,
            is_home_delivery: this.props.order.is_home_delivery || false,
        });
    }

    confirm() {
        this.props.getPayload({
            expected_delivery_date: this.state.expected_delivery_date,
            laundry_note: this.state.laundry_note,
            is_urgent: this.state.is_urgent,
            is_home_delivery: this.state.is_home_delivery,
        });
        this.props.close();
    }
}

export class LaundryLinePopup extends Component {
    static components = { Dialog };
    static template = "pos_laundry_management_ucs.LaundryLinePopup";
    static props = {
        close: Function,
        getPayload: Function,
        line: Object,
        washingTypes: Array,
    };

    setup() {
        this.pos = usePos();
        const initialType = this.props.line.washing_type_id 
            ? (this.props.line.washing_type_id.id || this.props.line.washing_type_id) 
            : "";
        this.state = useState({
            washing_type_id: initialType,
            laundry_item_note: this.props.line.laundry_item_note || "",
        });
    }

    confirm() {
        const selectedType = this.props.washingTypes.find(
            (t) => t.id === parseInt(this.state.washing_type_id)
        ) || false;
        this.props.getPayload({
            washing_type_id: selectedType,
            laundry_item_note: this.state.laundry_item_note,
        });
        this.props.close();
    }
}
