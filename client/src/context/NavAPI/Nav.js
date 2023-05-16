import Bus from "./Bus"
import Line from "./Line"
import Node from "./Node"
import Passenger from "./Passenger"

// FOR TESTING ONLY
const shapeId = {
    0: "Square",
    1: "Triangle",
    2: "Circle"
}

shrishella = new Passenger(0)
kimothy = new Passenger(1)
rajykins = new Passenger(2)

node1 = new Node(1);
node2 = new Node(2);
node3 = new Node(3);
node4 = new Node(4);
node5 = new Node(5);


line1 = new Line([node1, node3, node4]);
line2 = new Line([node2, node4, node5]);
line3 = new Line([node2, node4, node5, node2]);

lines = [line1, line2, line3]

bus = new Bus()

const passengerPath = (passenger) => {
    let queue = []
    let visited = new Set()
    let distances = []
    let paths = []

    let start = passenger.startNode

    queue.push(start)
    distances.push(0)
    paths.push([start.id])
    visited.add(start.id)

    while(true) {
        currentNode = queue.shift();
        currentDistance = distances.shift()
        currentPath = paths.shift();

        if(currentNode.shape == passenger.shape) {
            break;
        }

        for (let line in lines) {
            for (let n = 0; n < line.length; n++) {
                if (line[n].id == currentNode.id && isLoop(n, line)) {
                    if(!visited.has(line[1].id)) {
                        queue.push(line[1])
                        distances.push(currentDistance + 1)
                        paths.push(currentPath.push(line[1].id))
                        visited.add(line[1].id)
                    }
                    if(!visited.has(line[line.length-2].id)) {
                        queue.push(line[line.length-2])
                        distances.push(currentDistance + 1)
                        paths.push(currentPath.push(line[line.length-2].id))
                        visited.add(line[line.length-2].id)
                    }
                }
                else if (n == line.length-1) {
                    if(!visited.has(line[line.length-2].id)) {
                        queue.push(line[line.length-2])
                        distances.push(currentDistance + 1)
                        paths.push(currentPath.push(line[line.length-2].id))
                        visited.add(line[line.length-2].id)
                    }
                }
            }
        }
    }
}

//checks if line is in a loop
const isLoop = (n, line) => {
    return (n == 0 || n == line.length-1) && line[0] == line[line.length-1]
}

const findCar = (line, moves, bus) => {
    
}