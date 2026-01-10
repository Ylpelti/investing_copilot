import { getPortfolios } from "@/lib/api"
import { PortfolioList } from "@/components/portfolio/portfolioList"

export const PortfolioPage = async () => {
    const portfolios = await getPortfolios()
    return <PortfolioList portfolios={portfolios} />
}