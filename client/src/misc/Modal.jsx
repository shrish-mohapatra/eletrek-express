import React, { useContext } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'

import { TransportContext } from '../context/TransportProvider'

const Modal = () => {
    const { lines, getLineColor, generate, metrics, loading } = useContext(TransportContext)

    const renderMetrics = () => {
        if (!metrics) return
        return (
            <>
                <div className='metric'>
                    <p>Delivered passengers</p>
                    <p>{metrics.total_passengers - metrics.missed_passengers}/{metrics.total_passengers}</p>
                </div>
                <div className='metric'>
                    <p>Total path length</p>
                    <p>{metrics.path_length.toFixed(0)} m</p>
                </div>
                <div className='metric'>
                    <p>Avg. path length</p>
                    <p>{(metrics.path_length/(metrics.total_passengers-metrics.missed_passengers)).toFixed(0)} m</p>
                </div>
                <br/>
                <div className='metric'>
                    <p>Number of lines</p>
                    <p>{metrics.num_lines}</p>
                </div>
                <div className='metric'>
                    <p>Total line length</p>
                    <p>{metrics.line_length.toFixed(0)} m</p>
                </div>
            </>
        )
    }

    return (
        <div className='modal'>
            <h1>:: elektrek express</h1>

            <span>
                Developed by Josh Kim, Rajessen Sanassy, Shrish Mohapatra
            </span>

            <div className='lines'>
                {
                    lines.map((line, i) => (
                        <div
                            key={`line-label-${i}`}
                            className='line-label'
                            style={{ backgroundColor: getLineColor(i) }}
                        >
                            {i + 1}
                        </div>
                    ))
                }
            </div>

            {renderMetrics()}

            <div className='btn-group'>
                <button className="btn btn-clear">Learn more</button>
                <button
                    className="btn btn-primary"
                    onClick={generate}
                    disabled={loading}
                >
                    {
                        loading ? <FontAwesomeIcon icon={faSpinner} spin/> : "Regenerate"
                    }                    
                </button>
            </div>
        </div>
    )
}

export default Modal