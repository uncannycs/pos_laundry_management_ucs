import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Base } from "@point_of_sale/app/models/related_models";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

export class LaundryWashingType extends Base {
    static pythonModel = "laundry.washing.type";
}

registry.category("pos_available_models").add(LaundryWashingType.pythonModel, LaundryWashingType);


