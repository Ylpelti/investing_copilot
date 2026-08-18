import { TransactionRead, TransactionCreate } from "@/types/transaction";
import { authRequest } from "../requests/authRequest";
import { mockTransactions } from "../mock/transactionMockData";


export const getPortfolioTransactions = async (portfolio_id: number): Promise<TransactionRead[]> => {
    return mockTransactions.filter(t => t.portfolio_id === portfolio_id)
}

export const createTransaction = async (data: TransactionCreate) => {
    return authRequest("/transactions", {
        method: "POST",
        body: JSON.stringify(data)
    })
}
