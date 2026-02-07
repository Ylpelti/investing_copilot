"use server"
import { explainPortfolio } from "@/lib/api/portfolio"
import { PortfolioExplanation } from "@/types/portfolio"

export const explainPortfolioAction = async (portfolio_id:number): Promise<PortfolioExplanation> => {
    return explainPortfolio(portfolio_id)
}