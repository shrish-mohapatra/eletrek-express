export class Problem {
    constructor(passenger, lines, busses, startNode=null) {
        this.passenger = passenger
        this.lines = lines
        this.busses = busses
        this.startNode = passenger.startNode
    }

    is_goal(node) {
        return (node.shape == passenger.shape)
    }


    // Evaluation functions
    f(node) {
        return node.path_cost + this.heuristic_manhattan(node.position)
    }

    heuristic(distBus, position2=this.goal_position) {
        // distance of car + distance from current position to the goal
    }

    getAdjecentNodes(node) {
        // return all adjecent nodes from looking at lines
    }

    getWaitCost(node) {
        
    }
}

export default Problem