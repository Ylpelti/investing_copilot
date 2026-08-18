"use client"

import { AreaDataDTO } from "@/types/chartData"
import { AreaSeries, ChartOptions, createChart, DeepPartial } from "lightweight-charts"
import { useEffect, useRef } from "react"

type Props = {
    data: AreaDataDTO[],
    chartOptions: DeepPartial<ChartOptions>
}

const AreaChart = ({data, chartOptions}: Props) => {
    const containerRef = useRef<HTMLDivElement | null>(null)
    useEffect(() => {
        if (!containerRef.current || data.length === 0) return;
        const chart = createChart(containerRef.current, {
            width: 600,
            height: 300,
            ...chartOptions
        })
        const series = chart.addSeries(AreaSeries)
        series.setData(data)
        chart.timeScale().fitContent()
        return () => chart.remove() 

    }, [data, chartOptions])
    return (
        <div ref={containerRef}></div>
    )
}

export default AreaChart
