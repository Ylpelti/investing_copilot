import { StockOption } from "@/types/stock"
import { apiRequest } from "../requests/http"



export const searchStocks = async ( query: string, limit: number = 10): Promise<StockOption[]> => {
    return apiRequest<StockOption[]>(`/stocks/search?q=${encodeURIComponent(query)}&limit=${limit}`, {
        method: "GET",
    })
}