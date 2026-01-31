import { PortfolioRead } from "@/types/portfolio"
import Link from "next/link"

export const PortfolioList = ({ portfolios }: {portfolios: PortfolioRead[]}) => {
    return (
        <div>
            {portfolios.map(p => (
                <div key={p.id}>
                    <h1>{p.name}</h1>
                    <p>{p.description}</p>
                    <button>
                        <Link href={`/portfolios/${p.id}`}>Open portfolio</Link>
                    </button>
                </div>
            
            ))}
            
        </div>
    )
}