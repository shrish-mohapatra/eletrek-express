import React, { useEffect, useContext, useState } from 'react'
import { TransportContext } from '../context/TransportProvider';
import Bus from './Bus';

const MAP_OFFSET = 50

function Line({ id, color }) {
    const { nodes, lines, counter } = useContext(TransportContext)
    const [points, setPoints] = useState()
    const [busState, setBusState] = useState({ startIndex: 0, direction: 1 })
    const [prevCounter, setPrevCounter] = useState(-1)
    const strokeWidth = 3;

    useEffect(() => {
        if (nodes) {
            generatePoints()
        }
    }, [id, nodes])

    useEffect(() => {
        if (points && busState && counter != prevCounter) {
            setPrevCounter(counter)
            setBusState(curState => {
                let startIndex = curState.startIndex
                let direction = curState.direction
                let curPoints = {}

                startIndex += direction

                // Adjust direction
                if (startIndex < 0) {
                    startIndex = 0
                    direction = 1
                } else if (startIndex >= points.length) {
                    startIndex = points.length - 1
                    direction = -1
                }

                // Set curpoints
                if(direction == 1) {
                    curPoints.x1 = points[startIndex].x1
                    curPoints.y1 = points[startIndex].y1
                    curPoints.x2 = points[startIndex].x2
                    curPoints.y2 = points[startIndex].y2
                } else {
                    curPoints.x1 = points[startIndex].x2
                    curPoints.y1 = points[startIndex].y2
                    curPoints.x2 = points[startIndex].x1
                    curPoints.y2 = points[startIndex].y1
                }

                return { startIndex, direction, curPoints }
            })
        }
    }, [counter, points, busState, prevCounter])

    const generatePoints = () => {
        const newPoints = []

        for (let i = 1; i < lines[id].length; i++) {
            const curLine = lines[id]
            newPoints.push({
                x1: nodes[curLine[i - 1]].x,
                y1: nodes[curLine[i - 1]].y,
                x2: nodes[curLine[i]].x,
                y2: nodes[curLine[i]].y,
            })
        }

        setPoints(newPoints)
    }

    if (!points || !busState.curPoints) return <div />
    return (
        <>
            {
                points.map((p, i) => (
                    <>
                        <line
                            key={`line-${id}-${i}`}
                            x1={p.x1}
                            x2={p.x2}
                            y1={p.y1}
                            y2={p.y2}
                            stroke={color}
                            strokeWidth={strokeWidth}
                        />
                    </>
                ))
            }
            <Bus
                color={color}
                x1={points[0].x1}
                y1={points[0].y1}
                x2={points[0].x2}
                y2={points[0].y2}
                key={counter}
            />
        </>
    )
}

export default Line