import { StockPrice,  } from "@/types/stock";
import { CandleStickDataDTO, ChartData } from "@/types/chartData";

export const stockprice_to_candlestick = (prices: StockPrice[]): CandleStickDataDTO[] => {
    const normalized = prices.map(p => ({
        time: p.date,
        open: p.open_price,
        close: p.close_price,
        high: p.high_price,
        low: p.low_price,
    }))
    return normalized
}

export const stockprice_to_chartdata = (prices: StockPrice[]):ChartData[] => {
    return (
        prices.map(p => ({
            time: p.date,
            value: p.close_price
        }))
    )
}
