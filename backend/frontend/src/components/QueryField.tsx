import { useState } from "react"


const QueryField = ({ currentTable }) => {
    const [q, setQ] = useState("")

    const handleSubmit = async () => {
        const response = await fetch('http://localhost:8001/api/ask-question',
            {
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: q,
                    table_name: currentTable
                })
            })
            const result = await response.json()
            console.log(result)
    }

    return (
        <>
            <textarea
                value={q}
                onChange={e => setQ(e.target.value)}
                placeholder="Enter your question"
                className="textarea textarea-bordered textarea-lg w-[500px]" ></textarea>
            <button className="btn" onClick={handleSubmit}>Submit</button>
        </>
    )
}

export default QueryField