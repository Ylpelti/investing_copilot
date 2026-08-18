
import { PortfolioList } from "@/components/portfolio/portfolioList"
import { PortfolioForm } from "@/components/portfolio/portfolioForm"

import { getCurrentUser } from "@/lib/api/auth/auth"
import { getUserPortfolios } from "@/lib/api/portfolio"
import { createPortfolioAction } from "@/actions/portfolio/portfolioActions"




const PortfolioPage = async () => {
    
    const currentUser = await getCurrentUser()
    const portfolios = await getUserPortfolios()
    
    const boundCreatePortfolio = createPortfolioAction.bind(null, {
        userId: currentUser.id
    }) 

    
    return (
        <div>
        <PortfolioList portfolios={portfolios} />
        <PortfolioForm action={boundCreatePortfolio}/>
        </div>
    )
}

export default PortfolioPage
