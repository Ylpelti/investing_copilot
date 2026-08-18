"use client"

import type { ChartData } from "@/types/chartData"
import { BaselineSeries, ChartOptions, createChart, DeepPartial } from "lightweight-charts"
import { useEffect, useRef } from "react"

type Props = {
    data: ChartData[],
    chartOptions: DeepPartial<ChartOptions>
}

export const BaselineChart = ({data, chartOptions}: Props) => {
    const containerRef = useRef<HTMLDivElement | null>(null)
    useEffect(() => {
        if (!containerRef.current || data.length === 0) return;
        const chart = createChart(containerRef.current, {
            width: 600,
            height: 300,
            ...chartOptions
        })
        const series = chart.addSeries(BaselineSeries)
        series.setData(data)
        chart.timeScale().fitContent()
        
        return () => chart.remove()
    }, [data, chartOptions])
    return (
        <div ref={containerRef}></div>
    )
}
