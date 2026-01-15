'use client'

import { useActionState } from "react"

import { actionState } from "@/types/action"

type Props = {
    action: (
        prevState: actionState,
        formData: FormData
    ) => Promise<actionState>
}

const initialState: actionState = { success: false }

export const LoginForm = ({ action }: Props) => {
    const [state, formAction, isPending] = useActionState(
        action,
        initialState
    )
    
    return (
        <form action={formAction}>
            <h1>Login form</h1>
            <input type="text"
            placeholder="username"
            name="username" 
            />

            <input type="text"
            placeholder="password"
            name="password"
             />

            <button type="submit" disabled={isPending}> 
                {isPending ? "Login in..." : "Login"}
            </button>
                {state.error && <p>{state.error}</p>}
                
        </form>
    )
}