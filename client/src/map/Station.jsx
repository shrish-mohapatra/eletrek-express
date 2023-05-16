import React from 'react'
import Shape from './Shape'

const MAX_ROWS = 3
const shapes = ["triangle", "square", "circle"]

function Station({ shape, x, y, passengers }) {

    const getPassengerPos = (i) => {
        const x = 20 * (Math.floor(i / MAX_ROWS) + 1) + 20
        const y = 20 * (Math.floor(i % MAX_ROWS)) - 15
        return {x, y}
    }

    return (
        <>
            <Shape shape={shape} x={x} y={y} />
            {
                passengers.map((p, i) => (
                    <Shape
                        key={`passenger-${x}-${i}`}
                        shape={shapes[p]}
                        x={x-getPassengerPos(i).x}
                        y={y+getPassengerPos(i).y}
                        size={15}
                        strokeWidth={0}
                        fill="black"
                    />
                ))
            }

        </>

    );
}

export default Station