import { PortfolioRead, PortfolioCreate, PortfolioExplanation } from "@/types/portfolio"
import { authRequest } from "../requests/authRequest"
import { ChartData } from "@/types/chartData"


export const getUserPortfolios = async (): Promise<PortfolioRead[]> => {
    return authRequest<PortfolioRead[]>("/portfolios/me", {
        method: "GET"
    })
}

export const getPortfolioById = async (portfolio_id: number): Promise<PortfolioRead> => {
    return authRequest<PortfolioRead>(`/portfolios/${portfolio_id}`, {
        method: "GET",
    })
}

export const createPortfolio = async (data: PortfolioCreate): Promise<PortfolioRead> => {
    return authRequest<PortfolioRead>("/portfolios", {
        method: "POST",
        body: JSON.stringify(data)
    })
}

export const explainPortfolio = async (portfolio_id: number): Promise<PortfolioExplanation> => {
    return authRequest(`/portfolios/${portfolio_id}/explain`, {
        method: "POST"
    })
}

export const getPortfolioTimeserie = async (portfolio_id: number): Promise<ChartData[]> => {
    return authRequest(`/portfolios/${portfolio_id}/charts`, {
        method: "GET"
    })
}
