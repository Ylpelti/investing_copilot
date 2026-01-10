type TransactionType = "BUY" | "SELL"

type TransactionBase = {
    portfolio_id: number
    stock_id: number
    symbol:string
    type: TransactionType
    quantity: number
    price: number
    timestamp: string
}

export type TransactionRead = TransactionBase & {
    id:number
    total_value: number
}

