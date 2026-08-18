export type StockRead = {
    id: number
    ticker: string
    isin: string
    name: string
    sector: string
    updated_at: string
}

export type StockOption = {
  id: number
  symbol: string
  name: string
}

export type StockPrice = {
    stock_id: number
    date: string
    open_price: number
    high_price: number
    low_price: number
    close_price: number
    volume: number
}
