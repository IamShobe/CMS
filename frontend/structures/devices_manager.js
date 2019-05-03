import BaseManager from "./base_manager";

export class DevicesManager{
    constructor() {
        this.available = [];
        this.to_pair = [];
        this.paired = [];
        this.connected = [];
        this.renderAck = 0;
        this.address_to_name = {};
        this.phonebook = [];
    }

    get devices() {
        return [
            ...this.to_pair,
            ...this.paired,
            ...this.connected
        ]
    }

    updateNamesDict(list) {
        for (let device of list) {
            this.address_to_name[device.mac_address] = device.name;
        }
    }
    updatePhoneBook(phonebook) {
        this.phonebook = phonebook
    }

    update({pairable, paired, connected}) {
        let connected_dict = {};
        for (let device of connected) {
            connected_dict[device.mac_address] = device.name;
        }

        let paired_devices = [];
        for (let device of paired) {
            if (!(device.mac_address in connected_dict)) {
                paired_devices.push(device)
            }
        }

        this.to_pair = pairable;
        this.paired = paired_devices;
        this.connected = connected;
        this.updateNamesDict(this.to_pair);
        this.updateNamesDict(this.paired);
        this.updateNamesDict(this.connected);
        this.renderAck ++;
    }
}

const bluetooth = new DevicesManager();
export default bluetooth;
