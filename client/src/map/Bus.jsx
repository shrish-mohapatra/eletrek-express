import React, { useContext, useEffect, useState } from 'react'
import { TransportContext } from '../context/TransportProvider';

const BUS_LENGTH = 50
const TIME_FACTOR = 10

function generateLine(x1, y1, x2, y2, length) {
    // Calculate the length of the line
    const lineLength = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));

    // Calculate the unit vector of the line
    const unitX = (x2 - x1) / lineLength;
    const unitY = (y2 - y1) / lineLength;

    // Calculate the new endpoint coordinates
    const busX = x1 + unitX * length;
    const busY = y1 + unitY * length;

    // Return the new endpoint coordinates
    return { busX, busY, unitX, unitY, lineLength };
}

function Bus({ color, x1, y1, x2, y2 }) {
    const { counter } = useContext(TransportContext)
    const { busX, busY, unitX, unitY, lineLength } = generateLine(x1, y1, x2, y2, BUS_LENGTH)
    const strokeWidth = 3;

    const [busPos, setBusPos] = useState(1)

    useEffect(() => {
        setBusPos(1)
        const interval = setInterval(() => {
            setBusPos(curPos => curPos ? 0 : 1)
        }, Math.round(lineLength * TIME_FACTOR) + 1000)

        return () => clearInterval(interval)
    }, [x1])

    return (
        <line
            key={counter}
            className='bus'
            x1={x1}
            y1={y1}
            x2={busX}
            y2={busY}
            stroke={color}
            strokeWidth={strokeWidth * 4}
            transform={`translate(${Math.floor(unitX * busPos * (lineLength - BUS_LENGTH))}, ${Math.floor(unitY * busPos * (lineLength - BUS_LENGTH))})`}
            style={{transition: `all ${Math.round(lineLength * TIME_FACTOR)}ms linear`}}
        />
    )
}

export default Bus