import { StockOption } from "@/types/stock";
import { StockSearchInput } from "./stockSearchInput";
import { StockSearchResults } from "./stockSearchResult";
import { useState, useEffect } from "react";
import { stockSearchAction } from "@/actions/stockSearchAction";


type Props = {
  onSelect?: (stock: StockOption) => void
}

export const StockSearch = ({ onSelect }: Props) => {
    const [query, setQuery] = useState("")
    const [results, setResults] = useState<StockOption[]>([])
    const [loading, setLoading] = useState(false)

    useEffect(() => {
    if (query.length < 2) {
      setResults([])
      return
    }
    const timeout = setTimeout(async () => {
        setLoading(true)
        try {
            const data = await stockSearchAction(query, 10)
            setResults(data)
        } finally {
            setLoading(false)
        }

    }, 300)
    return () => clearTimeout(timeout)
}, [query])
    return (
        <div>
            <StockSearchInput value={query} onChange={setQuery} />
            <StockSearchResults results={results} loading={loading} onSelect={onSelect} />

        </div>
    )
}