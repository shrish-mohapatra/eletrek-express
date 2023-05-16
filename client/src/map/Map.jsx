import React, { useContext } from 'react'
import randomColor from 'randomcolor'
import Line from './Line'
import Station from './Station'

import { TransportContext } from '../context/TransportProvider'

const MAP_WIDTH = 800
const MAP_HEIGHT = 700

function Map() {
    const { nodes, lines, getLineColor } = useContext(TransportContext)

    return (
        <div className="subway" style={{ width: MAP_WIDTH, height: MAP_HEIGHT }}>
            <svg width={MAP_WIDTH} height={MAP_HEIGHT}>
                {
                    lines.map((l, i) => (
                        <Line
                            key={i}
                            id={i}
                            x1={nodes[l[0]].x}
                            x2={nodes[l[1]].x}
                            y1={nodes[l[0]].y}
                            y2={nodes[l[1]].y}
                            color={getLineColor(i)}
                        />
                    ))
                }
                {
                    nodes.map(({ shape, x, y, passengers }, i) => (
                        <Station
                            key={i}
                            shape={shape}
                            x={x}
                            y={y}
                            passengers={passengers}
                        />
                    ))
                }
            </svg>
        </div>
    )
}

export default Map