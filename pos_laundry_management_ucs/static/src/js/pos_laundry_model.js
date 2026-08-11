import { Base } from "@point_of_sale/app/models/related_models";
import { registry } from "@web/core/registry";
export class LaundryWashingType extends Base {
    static pythonModel = "laundry.washing.type";
}

registry.category("pos_available_models").add(LaundryWashingType.pythonModel, LaundryWashingType);


