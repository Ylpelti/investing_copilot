"use client"

import type { HistogramDataDTO } from "@/types/chartData"
import { ChartOptions, createChart, DeepPartial, HistogramSeries } from "lightweight-charts"
import { useRef, useEffect } from "react"

type Props = {
    data: HistogramDataDTO[],
    chartOptions: DeepPartial<ChartOptions>
}

export const HistogramChart = ({data, chartOptions}: Props) => {
    const containerRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        if (!containerRef.current || data.length === 0) return;

        const chart = createChart(containerRef.current, {
            width: 600,
            height: 300,
            ...chartOptions
        })
        const series = chart.addSeries(HistogramSeries)
        series.setData(data)
        return () => chart.remove()
    }, [data, chartOptions])
    return (
        <div ref={containerRef}></div>
    )

}
