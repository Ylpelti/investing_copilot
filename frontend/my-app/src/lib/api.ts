import { mockPortfolios } from "./portfolioMockData"
import { PortfolioRead } from "@/types/portfolio"

export const getPortfolios = async (): Promise<PortfolioRead[]> => {
    return mockPortfolios
}