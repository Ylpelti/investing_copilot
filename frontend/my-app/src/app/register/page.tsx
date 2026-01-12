"use client"

import { useState } from "react"



const RegisterPage = () => {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handeLogin = async (e: React.FormEvent) => {
        e.preventDefault()

        
    }

    return (
        <form onSubmit={handeLogin}>
            <h1>Register</h1>
            <input type="Username" 
                value={username}
                placeholder="username"
                onChange={e => setUsername(e.target.value)}/>

            <input type="email"
            value={email}
            placeholder="email"
            onChange={e => setEmail(e.target.value)} />

            <input type="password"
            value={password}
            placeholder="password"
            onChange={e => setPassword(e.target.value)} />

            <button type="submit">Register now</button>
        </form>
    )
} 

export default RegisterPage 