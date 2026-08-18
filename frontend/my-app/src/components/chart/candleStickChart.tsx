"use client"

import { CandlestickSeries, ChartOptions, createChart, DeepPartial } from "lightweight-charts";
import { useRef, useEffect } from "react";
import type { CandleStickDataDTO } from "@/types/chartData";

type Props = {
    data: CandleStickDataDTO[],
    options?: DeepPartial<ChartOptions>
}

export const CandleStickChart = ({data, options}: Props) => {
    const containerRef = useRef<HTMLDivElement | null>(null)
    useEffect(() => {
        if (!containerRef.current || data.length === 0) return;

        const chart = createChart(containerRef.current, {
            width: 600,
            height: 300,
            ...options
        })

        const series = chart.addSeries(CandlestickSeries)
        series.setData(data)
        chart.timeScale().fitContent()

        return () => chart.remove()
    }, [data, options])
    return (
        <div ref={containerRef}></div>
    )
}