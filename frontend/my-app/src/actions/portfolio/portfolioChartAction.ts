"use server"
import { getPortfolioTimeserie } from "@/lib/api/portfolio";

export const chartPortfolioAction = async (portfolio_id: number) => {
    return getPortfolioTimeserie(portfolio_id)
}