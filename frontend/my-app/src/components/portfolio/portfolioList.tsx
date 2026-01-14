import { PortfolioRead } from "@/types/portfolio"

export const PortfolioList = ({ portfolios }: {portfolios: PortfolioRead[]}) => {
    return (
        <div>
            {portfolios.map(p => (
                <div key={p.id}>
                    <h1>{p.name}</h1>
                    <p>{p.description}</p>
                </div>

            ))}
        </div>
    )
}