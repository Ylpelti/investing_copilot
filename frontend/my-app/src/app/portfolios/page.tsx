
import { PortfolioList } from "@/components/portfolio/portfolioList"
import { PortfolioForm } from "@/components/portfolio/portfolioForm"

import { getCurrentUser } from "@/lib/mock/userMockData"
import { getUserPortfolios } from "@/lib/mock/portfolioMockData"
import { createPortfolioAction } from "@/actions/portfolio_actions"




const PortfolioPage = async () => {
    
    const current_user_id = await getCurrentUser().id
    const portfolios = await getUserPortfolios(current_user_id)
    
    const boundCreatePortfolio = createPortfolioAction.bind(null, {
        userId: current_user_id
    }) 

    
    return (
        <div>
        <PortfolioList portfolios={portfolios} />
        <PortfolioForm action={boundCreatePortfolio}/>
        </div>
    )
}

export default PortfolioPage