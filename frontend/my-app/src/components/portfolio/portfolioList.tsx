import { PortfolioRead } from "@/types/portfolio"

export const PortfolioList = ({ portfolios }: {portfolios: PortfolioRead[]}) => {
    return (
        <ul>
            {portfolios.map(p => (
                <li key={p.id}>
                    <h1>{p.name}</h1>
                    <p>{p.description}</p>
                </li>

            ))}
        </ul>
    )
}