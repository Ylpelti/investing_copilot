
import { PositionTable } from "@/components/positions/positionList"
import { getPortfolioById } from "@/lib/api/portfolio"
import { getPositions } from "@/lib/api/position"
import { getPortfolioTransactions } from "@/lib/api/transactions"
import { TransactionList } from "@/components/portfolio/transactionList"
import { PositionForm } from "@/components/positions/positionForm"

import { getCurrentUser } from "@/lib/mock/userMockData"
import { createPositionAction } from "@/actions/position_action"


type PageProps = {
    params: Promise<{
        id: string
    }>
}

const PortfolioDetailPage = async ({ params }: PageProps) => {
    const { id } = await params
    const portfolioId = Number(id)
    const current_user_id = getCurrentUser().id
    
    const portfolio = await getPortfolioById(portfolioId)
    const positions = await getPositions(portfolioId)
    const transactions = await getPortfolioTransactions(portfolioId)

    
    const boundCreatePosition = createPositionAction.bind(null, {
        portfolioId,
        userId: current_user_id
    })
   
    return (
        <div>
            <h1>{portfolio.name}</h1>
            <PositionTable positions={positions}/>

            <h1>Transactions</h1>
            <TransactionList transactions={transactions} />

            <PositionForm action={boundCreatePosition} />
        </div>
        
    )
}

export default PortfolioDetailPage
