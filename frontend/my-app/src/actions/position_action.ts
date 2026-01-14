"use server"

import { revalidatePath } from "next/cache"
import { createMockPosition } from "@/lib/mock/positionMockData"
import type { PositionCreate } from "@/types/position"

type ActionContext = {
  portfolioId: number
  userId: number
}

export type CreatePositionState = {
  success: boolean
  error?: string
}

export async function createPositionAction(
  context: ActionContext,
  prevState: CreatePositionState,
  formData: FormData
): Promise<CreatePositionState> {
  try {
    const symbol = String(formData.get("symbol") ?? "").trim()
    const quantity = Number(formData.get("quantity"))
    const buy_price = Number(formData.get("buy_price"))

    if (!symbol) throw new Error("Symbol is required")
    if (quantity <= 0) throw new Error("Quantity must be greater than 0")
    if (buy_price <= 0) throw new Error("Buy price must be greater than 0")

    const payload: PositionCreate = {
      symbol,
      quantity,
      buy_price,
      portfolio_id: context.portfolioId,
      stock_id: 1, // derived server-side
    }

    await createMockPosition(payload)

    revalidatePath(`/portfolios/${context.portfolioId}`)

    return { success: true }
  } catch (e) {
    return {
      success: false,
      error: e instanceof Error ? e.message : "Unknown error",
    }
  }
}
