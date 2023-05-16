import PQNode from './PQNode'

export class PriorityQueue {
    constructor() {
        this.queue = [];
    }

    put(priority, value) {
        let node = new PQNode(priority, value);
        this.queue.push(node)
        this.queue = this.queue.sort((n1, n2) => n1.priority - n2.priority)
    }

    put(pqnode) {
        this.queue.push(pqnode)
        this.queue = this.queue.sort((n1, n2) => n1.priority - n2.priority)
    }

    get() {
        if (this.empty()) return -1
        return this.queue.shift()
    }

    empty() {
        return this.queue.length === 0
    }
}

export default PriorityQueue