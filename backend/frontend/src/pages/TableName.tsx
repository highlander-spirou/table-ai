import { useParams } from "react-router-dom"
import { useState, useEffect } from "react"
import QueryField from "../components/QueryField"

interface Data {
    columns: string[]
    data: any[]
}

const TableName = () => {
    const { tblName } = useParams()

    const [isLoading, toggleLoading] = useState(false)
    const [error, setError] = useState(false)
    const [data, setData] = useState<Data | null>(null)
    const [shouldDispatch, changeShouldDispatch] = useState(true)
    const [val, setVal] = useState<number>(1)

    const onChangeVal = (e) => {
        if (e.target.name === 'increase') {
            setVal(currentVal => { return currentVal + 1 })
            changeShouldDispatch(true)
        } else {
            setVal(currentVal => { return currentVal - 1 })
            changeShouldDispatch(true)
        }
    }


    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            changeShouldDispatch(true)
        }
    }

    useEffect(() => {
        if (shouldDispatch) {
            toggleLoading(true)
            fetch(`http://localhost:8001/api/table/${tblName}?page=${val}`)
                .then(response => {
                    if (response.ok) {
                        response.json().then(data => { setData(data) })
                    } else {
                        setError(true)
                    }
                }).finally(() => {
                    toggleLoading(false)
                })
            changeShouldDispatch(false)
        }
    }, [shouldDispatch])

    if (error) {
        return <p>error</p>
    }
    return (
        <>
            <div>TableName</div>
            <div className="flex flex-col items-center gap-10">
                <div className="overflow-x-auto w-[700px] border-2 rounded-xl mt-3">
                    <div className="flex gap-3 items-center justify-end my-5 mr-3">
                        <button className={`btn btn-xs btn-ghost ${val === 1 ? "hidden" : ""}`}
                            name="decrease"
                            onClick={e => onChangeVal(e)}>{"<"}</button>

                        <input type="text" className="input input-bordered input-xs w-10" value={val}
                            onChange={e => setVal(Number(e.target.value))}
                            onKeyUp={handleKeyPress} />

                        <button className="btn btn-xs btn-ghost"
                            name="increase"
                            onClick={e => onChangeVal(e)}>{">"}</button>
                    </div>
                    {isLoading ? <p>Loading ...</p> : <>

                        <table className="table table-sm table-pin-rows">
                            <thead>
                                <tr>
                                    {data?.columns.map((col, index) => {
                                        return <th key={index}>{col}</th>
                                    })}
                                </tr>
                            </thead>
                            <tbody>
                                {data?.data.map((row, index) => {
                                    return <tr key={index}>
                                        {row.map((cell, cellIndex) => {
                                            return <td key={cellIndex}>{cell}</td>
                                        })}
                                    </tr>
                                })}
                            </tbody>
                        </table>
                    </>
                    }
                </div>
                <QueryField currentTable={tblName}/>
            </div>

        </>
    )
}

export default TableName