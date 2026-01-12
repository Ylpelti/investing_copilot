"use client"

import { getPortfolios } from "@/lib/api/portfolio"
import { PortfolioList } from "@/components/portfolio/portfolioList"
import { PortfolioForm } from "@/components/portfolio/portfolioForm"
import { useEffect, useState } from "react"
import { PortfolioRead } from "@/types/portfolio"
import { createPortfolio } from "@/lib/api/portfolio"


type PortfolioFormData = {
    name: string
    description?: string
}

const PortfolioPage =  () => {
    const [portfolios, setPortfolios] = useState<PortfolioRead[]>([])

    useEffect(() => {
        getPortfolios().then(setPortfolios)
    }, [])

    const handleCreate = async (data: PortfolioFormData) => {
        const payload = {
            user_id: Number(getCurrentUser()),
            name: data.name,
            description: data.description
        }
        const created = await createPortfolio(payload)
        setPortfolios(prev => [...prev, created])
    }
    
    return (
        <div>
        <PortfolioList portfolios={portfolios} />
        <PortfolioForm onSubmit={handleCreate}/>
        </div>
    )
}

export default PortfolioPage