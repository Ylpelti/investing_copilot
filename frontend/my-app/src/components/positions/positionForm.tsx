"use client"

import { useActionState } from "react"
import type { CreatePositionState } from "@/actions/position_action"

type Props = {
  action: (
    prevState: CreatePositionState,
    formData: FormData
  ) => Promise<CreatePositionState>
}

const initialState: CreatePositionState = { success: false }

export function PositionForm({ action }: Props) {
  const [state, formAction, isPending] = useActionState(
    action,
    initialState
  )

  return (
    <form action={formAction}>
      <input name="symbol" placeholder="Symbol" required />
      <input name="quantity" type="number" min={1} required />
      <input name="buy_price" type="number" step="0.01" min={0} required />

      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Add position"}
      </button>

      {state.error && <p>{state.error}</p>}
      {state.success && <p>Position added</p>}
    </form>
  )
}
