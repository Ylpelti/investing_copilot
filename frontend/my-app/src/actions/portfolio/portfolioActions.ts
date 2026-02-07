"use server"

import { revalidatePath } from "next/cache"
import { PortfolioCreate } from "@/types/portfolio"
import { createPortfolio } from "@/lib/api/portfolio"

type actionContext = {
    userId:number
}

export type CreatePortfolioState = {
    success: boolean
    error?: string
}

export const createPortfolioAction = async (
    context: actionContext,
    prevState: CreatePortfolioState,
    formData: FormData
): Promise<CreatePortfolioState> => {
    try {
        const name = String(formData.get("name") ?? "undefined").trim()
        const description = String(formData.get("description") ?? "undefined").trim()

        const payload: PortfolioCreate = {
        name,
        description,
        user_id: context.userId
    }
    if (!name) throw new Error("Name required")
    


    await createPortfolio(payload)
    revalidatePath('/portfolios')

    return { success: true}

    } catch(e) {
        return {
            success: false,
            error: e instanceof Error ? e.message : "unknown error"
        }
    }

    
}