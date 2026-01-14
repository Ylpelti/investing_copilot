type PositionBase = {
    symbol: string
    quantity: number
    portfolio_id: number
    stock_id: number
    buy_price: number
}

export type PositionFormData = {
    symbol: string
    quantity: number
    buy_price: number
}

export type PositionCreate = PositionBase

export type PositionRead = PositionBase & {
    id: number
}