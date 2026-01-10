import { TransactionRead } from "@/types/transaction";
import { mockTransactions } from "../mock/transactionMockData";

export const getPortfolioTransactions = async (portfolio_id: number): Promise<TransactionRead[]> => {
    return mockTransactions.filter(t => t.portfolio_id === portfolio_id)
}