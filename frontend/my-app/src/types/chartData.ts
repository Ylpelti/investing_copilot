

export type ChartData = {
    time: string
    value: number
}

export type CandleStickDataDTO = {
    time: string,
    open: number,
    close: number,
    high: number,
    low: number
}

export type HistogramDataDTO = {
    value: number,
    time: string
}

export type AreaDataDTO = {
    value: number,
    time: string
}