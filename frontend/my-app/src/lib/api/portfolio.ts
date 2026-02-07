import { PortfolioRead, PortfolioCreate, PortfolioExplanation } from "@/types/portfolio"
import { apiRequest } from "../requests/http"
import { authRequest } from "../requests/authRequest"


export const getUserPortfolios = async (): Promise<PortfolioRead[]> => {
    
    return authRequest<PortfolioRead[]>("/portfolios/me", {
        method: "GET"
    })
}

export const getPortfolioById = async (portfolio_id: number): Promise<PortfolioRead> => {
    console.log("Trying fetch portfolio with id:", portfolio_id);
    return authRequest<PortfolioRead>(`/portfolios/${portfolio_id}`, {
        method: "GET",
    })
}

export const createPortfolio = async (data: PortfolioCreate): Promise<PortfolioRead> => {
    console.log("Portfolio data before request: ", data);
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