export class PQNode {
    constructor(priority, value, purePath=0, path=[value.id]) {
        this.priority = priority; //total path_cost
        this.value = value;
        this.purePath = purePath; //path cost without wait time
        this.path = path
    }
}

export default Node