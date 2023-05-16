import React, { createContext, useEffect, useState } from 'react'
import { testNodes, testLines } from "../testMap.json"

const API_SERVER = "http://localhost:5000"

const lineColors = [
    '#FF4500', // orange red
    '#00CED1', // dark turquoise
    '#FFD700', // gold
    '#800080', // purple
    '#00FA9A', // medium spring green
    '#1E90FF', // dodger blue
    '#FF1493', // deep pink
    '#FF8C00', // dark orange
    '#9400D3', // dark violet
    '#228B22', // forest green
    '#8B0000', // dark red
    '#008080', // teal
    '#FF69B4'  // hot pink
]
let colorPointer = Math.floor(Math.random() * lineColors.length)

export const TransportContext = createContext()

export const TransportProvider = ({ children }) => {
    const [nodes, setNodes] = useState(testNodes)
    const [lines, setLines] = useState(testLines)
    const [metrics, setMetrics] = useState(null)
    
    const [counter, setCounter] = useState(0)
    const [loading, setLoading] = useState(false)

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         setCounter(counter => counter + 1)
    //     }, 2000)

    //     return () => clearInterval(interval)
    // }, [])

    return (
        <TransportContext.Provider
            value={{
                nodes, setNodes,
                lines, setLines,
                metrics,

                counter,

                lineColors, colorPointer,
                getLineColor: (lineIndex) => {
                    return lineColors[(colorPointer + lineIndex) % lineColors.length]
                },

                loading,
                generate: () => {
                    setLoading(true)
                    fetch(`${API_SERVER}/generate`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            map_width: 700,
                            max_passengers: 6,
                            space_between: 150,
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        const newNodes = []
                        for (let i in data.nodes) {
                            newNodes.push({
                                ...data.nodes[i],
                                x: data.nodes[i].x + 50,
                                y: data.nodes[i].y + 50,
                            })
                        }
                        setCounter(counter => counter + 1)
                        setNodes(newNodes)
                        setLines(data.lines)
                        setMetrics(data.metrics)
                        setLoading(false)
                        colorPointer = Math.floor(Math.random() * lineColors.length)
                    })
                    .catch(error => console.error(error))
                },
            }}
        >
            {children}
        </TransportContext.Provider>
    )
}