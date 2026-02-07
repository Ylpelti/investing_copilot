import * as z from "zod"

export const PositionReadSchema = z.object({
    symbol: z.string(),
    quantity: z.string(),
    portfolio_id: z.number(),
    stock_id: z.number(),
    buy_price: z.string(),
    id: z.number()
})


