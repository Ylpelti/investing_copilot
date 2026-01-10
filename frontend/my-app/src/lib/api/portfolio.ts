import { mockPortfolios } from "../mock/portfolioMockData"
import { PortfolioRead } from "@/types/portfolio"


export const getPortfolios = async (): Promise<PortfolioRead[]> => {
    return mockPortfolios
}

export const getPortfolioById = async (portfolio_id: number): Promise<PortfolioRead> => {
    const portfolio = mockPortfolios.find(p => p.id === portfolio_id)
    if (!portfolio) {
        throw new Error("Couldn't find portfolio with that id")
    }
    return portfolio
}