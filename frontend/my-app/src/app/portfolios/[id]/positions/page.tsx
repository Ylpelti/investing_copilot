import { getPositions } from "@/lib/api/position"
import { PositionTable } from "@/components/positions/positionList"

type PageProps = {
    params: {
        id: string
    }
}

export default async function PortfolioPositionsPage  ({ params } : PageProps)  {
    const { id } = await params
    const portfolioId = Number(id)
    console.log(portfolioId);
    const positions = await getPositions(portfolioId)
    return (
        <PositionTable positions={positions} />
    )
}

