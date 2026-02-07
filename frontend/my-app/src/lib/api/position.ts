import { PositionRead } from "@/types/position";
import { authRequest } from "../requests/authRequest";
import { authRequestWithSchema } from "../requests/authRequestWithSchema";
import { requestWithSchema } from "../requests/fetchAndParse";
import { PositionReadSchema } from "../schemas/position";

export const getPortfolioPositions = async (portfolio_id: number): Promise<PositionRead[]> => {
    return requestWithSchema(() => authRequestWithSchema(`/portfolios/${portfolio_id}/positions`, {
        method: "GET"
    }), PositionReadSchema.array())
    
}

