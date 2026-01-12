'use client'


import { useState } from "react"

type PortfolioFormData = {
    name: string
    desciption?: string
}

type Props = {
    onSubmit: (data: PortfolioFormData ) => void
}



export const PortfolioForm = ({ onSubmit }: Props) => {
    const [form, setForm] = useState({
        name: "",
        desciption: ""
    })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(form)
    }

    return (
        <form action="">
            <h1>Add new portfolio</h1>

            <input type="text"
            placeholder="Portfolio name"
            value={form.name}
            onChange={e => setForm({...form, name: e.target.value})} />

            <input type="text"
            placeholder="Descirption"
            value={form.desciption}
            onChange={e => setForm({...form, desciption: e.target.value})} />


            <button onSubmit={handleSubmit}> Add new portfolio</button>
        </form>
    )
}