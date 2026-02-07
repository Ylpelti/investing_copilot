'use client'

import  { CreatePortfolioState } from "@/actions/portfolio/portfolioActions"
import { useActionState } from "react"



type Props = {
    action: (
        prevState: CreatePortfolioState,
        formData: FormData
    ) => Promise<CreatePortfolioState>
}

const initialState: CreatePortfolioState = { success: false}

export const PortfolioForm = ({ action }: Props) => {
    const [state, formAction, isPending] = useActionState(
        action,
        initialState
    )

    

    return (
        <form action={formAction}>
            <h1>Add new portfolio</h1>

            <input name="name" placeholder="name" />
            <input name="description" placeholder="description" />

            <button type="submit" disabled={isPending}>
                {isPending ? "Saving..." : "Add new portfolio"}
            </button>

            
            {state.error && <p>{state.error}</p>}
            {state.success && <p>Portfolio added</p>}
        </form>
    )
}