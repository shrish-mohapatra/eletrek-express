export class Bus {
    constructor(line, direction=1, curNode, passengers=[]) {
        this.line = line
        this.direction = direction
        this.curNode = curNode
        this.passengers = passengers
    }
}

export default Bus