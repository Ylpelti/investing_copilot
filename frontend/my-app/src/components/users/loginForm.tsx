'use client'

import { useState } from "react"
import { UserLogin } from "@/types/user"

type Props = {
    onSubmit: (data: UserLogin) => void
}

export const LoginForm = ({ onSubmit }: Props) => {
    const [form, setForm] = useState<UserLogin>({
        username: "",
        password: ""
    })

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit(form)
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>Login form</h1>
            <input type="text"
            placeholder="username" 
            value={form.username}
            onChange={e => setForm({...form, username: e.target.value})}/>

            <input type="text"
            placeholder="password"
            value={form.password}
            onChange={e => setForm({...form, password: e.target.value})} />

            <button type="submit"> Login </button>

        </form>
    )
}