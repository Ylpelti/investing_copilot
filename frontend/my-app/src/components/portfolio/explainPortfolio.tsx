"use client"

import { useState, useTransition } from "react"
import { explainPortfolioAction } from "@/actions/portfolio/portfolioExplainAction"

type Props = {
  portfolioId: number
}

export const PortfolioExplanation = ({ portfolioId }: Props) => {
  const [explanation, setExplanation] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isPending, startTransition] = useTransition()

  const handleExplain = () => {
    setError(null)

    startTransition(async () => {
      try {
        const res = await explainPortfolioAction(portfolioId)
        setExplanation(res.explanation)
      } catch {
        setError("Failed to generate explanation")
      }
    })
  }

  return (
    <div>
      <button onClick={handleExplain} disabled={isPending}>
        {isPending ? "Explaining..." : "Explain portfolio"}
      </button>

      {error && <p>{error}</p>}
      {explanation && <p>{explanation}</p>}
    </div>
  )
}
