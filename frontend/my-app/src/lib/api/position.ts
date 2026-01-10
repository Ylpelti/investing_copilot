import { PositionRead } from "@/types/position";
import { mockPositions } from "../mock/positionMockData";

export const getPositions = async (portfolio_id: number): Promise<PositionRead[]> => {
    return mockPositions.filter(p => p.portfolio_id === portfolio_id)
}