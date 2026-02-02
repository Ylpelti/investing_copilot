import { PositionRead } from "@/types/position";
import { mockPositions } from "../mock/positionMockData";
import { authRequest } from "../requests/authRequest";



export const getPortfolioPositions = async (portfolio_id: number): Promise<PositionRead[]> => {
    return authRequest<PositionRead[]>("/", {
        method="GET"
    })
}