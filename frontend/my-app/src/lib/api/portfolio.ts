import * as mock from "../mock/portfolioMockData"
import { PortfolioRead, PortfolioCreate } from "@/types/portfolio"


export const getPortfolios = async (): Promise<PortfolioRead[]> => {
    return mock.mockPortfolios
}

export const getPortfolioById = async (portfolio_id: number): Promise<PortfolioRead> => {
    const portfolio = mock.mockPortfolios.find(p => p.id === portfolio_id)
    if (!portfolio) {
        throw new Error("Couldn't find portfolio with that id")
    }
    return portfolio
}

export const createPortfolio = async (data: PortfolioCreate): Promise<PortfolioRead> => {
    return 
}