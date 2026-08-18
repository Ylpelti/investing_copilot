import { getPortfolioPositions } from "@/lib/api/position"
import { PositionTable } from "@/components/positions/positionList"

type PageProps = {
    params: Promise<{
        id: string
    }>
}

export default async function PortfolioPositionsPage  ({ params } : PageProps)  {
    const { id } = await params
    const portfolioId = Number(id)
    const positions = await getPortfolioPositions(portfolioId)
    return (
        <PositionTable positions={positions} />
    )
}
