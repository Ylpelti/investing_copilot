"use client"

import { useActionState, useState } from "react"
import type { CreatePositionState } from "@/actions/transaction_action"
import { StockSearch } from "../stock/search/stockSearch"
import { StockOption } from "@/types/stock"

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
  const [selectedStock, setSelectedStock] = useState<StockOption | null>(null)

  return (
    <form action={formAction}>
      <StockSearch onSelect={stock => setSelectedStock(stock)} />
        <input type="hidden" name="stock_id" value={selectedStock?.id ?? ""} />
      <input name="quantity" type="number" placeholder="quantity" min={1} required />
      <input name="buy_price" type="number" placeholder="buy price" step="0.01" min={0} required />
      <select name="type" id="type">
        <option value="Buy">Buy</option>
        <option value="Sell">Sell</option>
      </select> 

      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Add position"}
      </button>

      {state.error && <p>{state.error}</p>}
      {state.success && <p>Position added</p>}
    </form>
  )
}
