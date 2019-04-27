import BaseManager from "./base_manager";

export default class DevicesManager extends BaseManager{
    constructor() {
        super();
        this.devices = {};
    }

    update(devices) {
        this.devices = devices;
        this.sync_number++;
        this.call_callbacks();
    }

}