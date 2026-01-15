"use client"

import { useActionState } from "react"
import type { CreateUserState } from "@/actions/user_actions"

type Props = {
  action: (
    prevState: CreateUserState,
    formData: FormData
  ) => Promise<CreateUserState>
}

const initialState: CreateUserState = { success: false }

export const RegisterForm = ({ action }: Props) => {
  const [state, formAction, isPending] = useActionState(
    action,
    initialState
  )

  return (
    <form action={formAction}>
      <h1>Register</h1>

      <input
        type="text"
        placeholder="username"
        name="username"
        required
      />

      <input
        type="email"
        placeholder="email"
        name="email"
        required
      />

      <input
        type="password"
        placeholder="password"
        name="password"
        required
      />

      <button type="submit" disabled={isPending}>
        {isPending ? "Registering..." : "Register now"}
      </button>

      {state.error && <p>{state.error}</p>}
      {state.success && <p>Registration complete</p>}
    </form>
  )
}
