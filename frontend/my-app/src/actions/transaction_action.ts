"use server"

import { revalidatePath } from "next/cache"
import { createMockPosition } from "@/lib/mock/positionMockData"
import { createTransaction } from "@/lib/api/transactions"
import { TransactionCreate, TransactionType } from "@/types/transaction"

type ActionContext = {
  portfolioId: number
  userId: number
}

export type CreatePositionState = {
  success: boolean
  error?: string
}

export async function createTransactionAction(
  context: ActionContext,
  prevState: CreatePositionState,
  formData: FormData
): Promise<CreatePositionState> {
  try {
    const symbol = String(formData.get("symbol") ?? "").trim()
    const quantity = Number(formData.get("quantity"))
    const buy_price = Number(formData.get("buy_price"))
    const rawType = String(formData.get("type"))

    if (!symbol) throw new Error("Symbol is required")
    if (quantity <= 0) throw new Error("Quantity must be greater than 0")
    if (buy_price <= 0) throw new Error("Buy price must be greater than 0")
    
    let type:TransactionType

    if (rawType == "Buy") {
      type = TransactionType.BUY
    } else if(rawType == "Sell") {
      type = TransactionType.SELL
    } else {
      throw new Error("Invalid transaction type")
    }
    
    const payload: TransactionCreate = {
      portfolio_id: context.portfolioId,
      stock_id: 1,
      symbol,
      type,
      quantity,
      price: buy_price
    }
    
    await createTransaction(payload)

    revalidatePath(`/portfolios/${context.portfolioId}`)

    return { success: true }
  } catch (e) {
    return {
      success: false,
      error: e instanceof Error ? e.message : "Unknown error",
    }
  }
}
