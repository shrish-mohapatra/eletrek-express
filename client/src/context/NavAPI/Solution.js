import Node from './Node'
import { PQNode } from './PQNode'
import PriorityQueue from './PriorityQueue.js'

export class Solution {
    constructor(problem) {
        this.problem = problem
    }

    dijkstra() {
        // frontier are next nodes to explore and reached is nodes already visited
        let frontier = new PriorityQueue()
        let reached = new Map([[this.problem.startNode.id, 0]])

        frontier.put(new PQNode(0, this.problem.startNode))

        while (!frontier.empty()) {
            node = frontier.get()

            // if we reached the goal, we return the path
            if (this.problem.is_goal(node.value)) return node.path
            const children = this.expand(node)

            for (let c in children) {
                const child = c.value
                // for each candidate, replace old priorities with new shorter ones
                // put it into the frontier
                if (!(child.id in reached) || c.priority < reached[child.id]) {
                    reached.set(child.id, c.priority)
                    frontier.put(c)
                }
            }
        }

        // No solution
        return -1
    }

    expand(node) {
        const children = []
        const nextNodes = this.problem.getAdjecentNodes(node.value)
        
        // for each candidate, change them into proper pqnodes
        for (let n in nextNodes) {
            let purePath = node.purePath + 1
            let waitCost = this.problem.getWaitCost(node)
            children.push(new PQNode(purePath + waitCost, n, purePath, node.path.concat([n.id])))
        }

        return children
    }

    hash_position(position) {
        return position.x.toString() + "," + position.y.toString()
    }
}

export default Solution