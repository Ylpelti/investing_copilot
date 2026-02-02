import { PositionRead } from "@/types/position";
import { authRequest } from "../requests/authRequest";



export const getPortfolioPositions = async (portfolio_id: number): Promise<PositionRead[]> => {
    console.log("Fecting positions from portfolio id: ", portfolio_id);
    return authRequest<PositionRead[]>(`/portfolios/${portfolio_id}/positions`, {
        method: "GET"
    })
}

