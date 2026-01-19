import { getCurrentUser } from "@/lib/api/auth/auth"
import { getUserPortfolios } from "@/lib/api/portfolio"
import { PortfolioList } from "@/components/portfolio/portfolioList"
import Link from "next/link"

const MePage = async () => {
    const user = await getCurrentUser()
    const portfolios = await getUserPortfolios()
    return (
        <div>
        <p>{user.username}</p>
        <p>{user.email}</p>
        <PortfolioList portfolios={portfolios} />
        <button>
        <Link href="/portfolios">Create new portfolio</Link>
        </button>
        </div>
    )
}

export default MePage