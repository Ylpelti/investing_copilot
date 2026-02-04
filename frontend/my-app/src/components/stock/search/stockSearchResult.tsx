import { StockOption } from "@/types/stock";

type Props = {
  results: StockOption[]
  loading: boolean
  onSelect?: (stock: StockOption) => void
}

export const StockSearchResults = ({ results, loading, onSelect}: Props) => {
    if (loading) {
        return (
            <div>
                ...loading
            </div>
        )
    }
    return (
        <ul>
            {results.map(stock => (
                <li key={stock.id}
                onClick={() => onSelect?.(stock)}>
                    <div>{stock.name}</div>
                    <div>{stock.symbol}</div>
                </li>
            ))}
        </ul>
    )
}