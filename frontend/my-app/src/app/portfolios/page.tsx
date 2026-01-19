
import { PortfolioList } from "@/components/portfolio/portfolioList"
import { PortfolioForm } from "@/components/portfolio/portfolioForm"

import { getCurrentUser } from "@/lib/mock/userMockData"
import { getUserPortfolios } from "@/lib/api/portfolio"
import { createPortfolioAction } from "@/actions/portfolio_actions"




const PortfolioPage = async () => {
    
    const current_user_id = await getCurrentUser().id
    const portfolios = await getUserPortfolios()
    
    const boundCreatePortfolio = createPortfolioAction.bind(null, {
        userId: current_user_id
    }) 

    
    return (
        <div>
        
        <PortfolioForm action={boundCreatePortfolio}/>
        </div>
    )
}

export default PortfolioPage