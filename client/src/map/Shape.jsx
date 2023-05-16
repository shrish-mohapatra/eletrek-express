import React from 'react'

function Shape({ shape, x, y, size=50, strokeWidth=3, fill="white", cn="", tf="" }) {
    const halfSize = size / 2;

    const pointsMap = {
        'triangle': `${x},${y - halfSize + 3} ${x - halfSize},${y + halfSize} ${x + halfSize},${y + halfSize}`,
        'square': `${x - halfSize},${y - halfSize} ${x + halfSize},${y - halfSize} ${x + halfSize},${y + halfSize} ${x - halfSize},${y + halfSize}`,
    }

    return (
        <>
            {pointsMap.hasOwnProperty(shape) ?
                <polygon
                    className={cn}
                    transform={tf}
                    points={pointsMap[shape]}
                    fill={fill}
                    stroke="black"
                    strokeWidth={strokeWidth}
                />
                :
                <circle
                    className={cn}
                    transform={tf}
                    cx={x}
                    cy={y}
                    r={size / 2}
                    fill={fill}
                    stroke="black"
                    strokeWidth={strokeWidth}
                />
            }
        </>

    );
}

export default Shape