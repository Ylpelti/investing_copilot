"use server"

import { searchStocks } from "@/lib/api/stock"
import { StockOption } from "@/types/stock"

export const stockSearchAction = async (query:string, limit?: number):Promise<StockOption[]> => {
    if (query.length < 2) {
        return []
    } 
    return searchStocks(query, limit)
}