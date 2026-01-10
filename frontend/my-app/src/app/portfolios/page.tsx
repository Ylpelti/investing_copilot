import { getPortfolios } from "@/lib/api/portfolio"
import { PortfolioList } from "@/components/portfolio/portfolioList"

const PortfolioPage = async () => {
    const portfolios = await getPortfolios()
    return <PortfolioList portfolios={portfolios} />
}

export default PortfolioPage