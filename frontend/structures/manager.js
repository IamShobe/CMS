import DevicesManager from "./devices_manager";
import BaseManager from "./base_manager";

export default class Manager extends BaseManager {
    constructor() {
        super();
        this.devices = new DevicesManager()
    }
}