import { StockOption, StockPrice, StockRead } from "@/types/stock"
import { apiRequest } from "../requests/http"



export const searchStocks = async ( query: string, limit: number = 10): Promise<StockOption[]> => {
    const stocks = await apiRequest<StockRead[]>(`/stocks/?q=${encodeURIComponent(query)}&limit=${limit}`, {
        method: "GET",
    })

    return stocks.map((stock) => ({
        id: stock.id,
        symbol: stock.ticker,
        name: stock.name,
    }))
}

export const getStockPrice = async (stock_id: number): Promise<StockPrice> => {
    return apiRequest<StockPrice>(`/stocks/${stock_id}/prices/latest`, {
        method: "GET"
    })
}
