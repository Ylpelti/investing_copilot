export enum TransactionType  {
    BUY = "BUY",
    SELL = "SELL"
}

type TransactionBase = {
    portfolio_id: number
    stock_id: number
    symbol:string
    type: TransactionType
    quantity: number
    price: number
}

export type TransactionRead = TransactionBase & {
    id:number
    total_value: number
}

export type TransactionCreate = TransactionBase

export type TransactionFormData = {
    ticker: string
    quantity: number
    buy_price: number
    type: TransactionType
}
