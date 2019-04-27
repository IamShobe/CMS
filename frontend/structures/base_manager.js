
export default class BaseManager {
    constructor() {
        this.callbacks = [];
        this.sync_number = 0;
    }
    register_callback(entity, callback, predicate) {
        this.callbacks.push({
            callback,
            predicate,
            entity
        })
    }
    call_callbacks() {
        for (let index in this.callbacks) {
            if (this.callbacks[index].predicate(this)) {
                this.callbacks[index].callback(this);
            }
        }
    }
}