type PortfolioBase = {
    name:string
    description?: string | null
}


export type PortfolioRead = PortfolioBase & {
    id: number
    user_id: number
    created_at: string
    updated_at:string
}

export type PortfolioCreate = PortfolioBase & {
    user_id:number
}

export type PortfolioExplanation = {
    portfolio_id: number
    explanation: string
}

