
import { PortfolioList } from "@/components/portfolio/portfolioList"
import { PortfolioForm } from "@/components/portfolio/portfolioForm"

import { getCurrentUser } from "@/lib/mock/userMockData"
import { getUserPortfolios } from "@/lib/api/portfolio"
import { createPortfolioAction } from "@/actions/portfolio/portfolioActions"




const PortfolioPage = async () => {
    
    const current_user_id = await getCurrentUser().id
    const portfolios = await getUserPortfolios()
    
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
