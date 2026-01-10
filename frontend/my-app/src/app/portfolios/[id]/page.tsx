import { PositionTable } from "@/components/positions/positionList"
import { getPortfolioById } from "@/lib/api/portfolio"
import { getPositions } from "@/lib/api/position"

type PageProps = {
    params: Promise<{
        id: string
    }>
}

const PortfolioDetailPage = async ({ params }: PageProps) => {
    const { id } = await params
    const portfolioId = Number(id)
    const portfolio = await getPortfolioById(portfolioId)
    const positions = await getPositions(portfolioId)
    return (
        <div>
            <h1>{portfolio.name}</h1>
            <PositionTable positions={positions}/>
        </div>
    )
}

export default PortfolioDetailPage
