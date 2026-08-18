export enum TransactionType  {
    BUY = "BUY",
    SELL = "SELL"
}

export type TransactionCreate = {
    portfolio_id: number
    stock_id: number
    type: TransactionType
    quantity: number
    price: number
    timestamp: Date
}

export type TransactionRead = {
    id:number
    portfolio_id: number
    stock_id: number
    type: TransactionType
    quantity: string
    price: string
    total_value: string
    timestamp: string
}

export type TransactionFormData = {
    stock_id: number
    quantity: number
    buy_price: number
    type: TransactionType
}
