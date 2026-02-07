export enum TransactionType  {
    BUY = "BUY",
    SELL = "SELL"
}

type TransactionBase = {
    portfolio_id: number
    stock_id: number
    type: TransactionType
    quantity: number
    price: number
    timestamp: Date
}

export type TransactionRead = TransactionBase & {
    id:number
    total_value: number
}

export type TransactionCreate = TransactionBase

export type TransactionFormData = {
    stock_id: number
    quantity: number
    buy_price: number
    type: TransactionType
}
