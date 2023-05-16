const MAP_WIDTH = 700
const MAP_HEIGHT = 600

/**
 * Generate nodes to represent subway map
 * @returns nodes, lines
 */
const generateMap = () => {
    const nodeCount = Math.random() * 3 + 5
    const lineCount = Math.random() * 3 + 8
    const shapeOptions = ["triangle", "square", "circle"]
    const nodes = []
    let lines = []

    // Generate nodes (stations)
    for (let i = 0; i < nodeCount; i++) {
        const { x, y } = generatePos(nodes)
        nodes.push({
            shape: shapeOptions[Math.floor(Math.random() * shapeOptions.length)],
            x, y,
        })
    }

    // Generate lines

    return { nodes, lines }
}

/**
 * Generate random node position
 * Ensure position does not overlap with others
 * @param {*} nodes 
 * @returns x,y
 */
const generatePos = (nodes) => {
    let x;
    let y;

    do {
        x = Math.random() * MAP_WIDTH
        y = Math.random() * MAP_HEIGHT
    } while (doesPosOverlap(nodes, x, y))

    return { x, y }
}

/**
 * Check if position overlaps with other nodes or out of bounds
 * @param {*} nodes 
 * @param {*} x 
 * @param {*} y 
 * @returns 
 */
const doesPosOverlap = (nodes, x, y) => {
    const threshold = 100

    // Check overlap with bounds
    if (x < threshold / 2 || (MAP_WIDTH - x) < threshold / 2) return true
    if (y < threshold / 2 || (MAP_HEIGHT - y) < threshold / 2) return true

    // Check overlap with other nodes
    for (let n in nodes) {
        if (manhattan_dist(nodes[n].x, x, nodes[n].y, y) < threshold) {
            return true
        }
    }

    return false
}

/**
 * Manhattan distance formula
 * @param {*} x1 
 * @param {*} x2 
 * @param {*} y1 
 * @param {*} y2 
 * @returns 
 */
const manhattan_dist = (x1, x2, y1, y2) => {
    return Math.abs(x1 - x2) + Math.abs(y1 - y2)
}