# Phase 1

## Passenger Logic
#### Constraints
- passenger has a goal destination/shape
- as soon as they reach any shape that matches, they get off (goal)
- passenger cannot start at same shape

```js

class Passenger {
    shape,
    ... // modify as needed
}

class Node {
    shape
    passengers = []
    x, y // <- only for display
}

class Line {
    connectedNodes = []
}

class Bus {
    line
    direction
    curNode
    passengers = []
}

shapes = [triangle, square, circle]


// global vars
lines = []
nodes = []
bus = []

// Assume every time we call `nextMove()`
//  - iteration increases by 1
//  - chooseTrain() will be called

function chooseTrain(passenger, iteration) {
    // decide which train passenger should take
    // if color-train cannot be reached, passenger will wait
    return bus
}
```