import { TransactionRead, TransactionType } from "../../types/transaction"

export const mockTransactions: TransactionRead[] = [
  {
    id: 1,
    portfolio_id: 1,
    stock_id: 101,
    type: TransactionType.BUY,
    quantity: "10",
    price: "150.00",
    total_value: "1500.00",
    timestamp: "2024-01-05T14:30:00Z"
  },
  {
    id: 2,
    portfolio_id: 1,
    stock_id: 101,
    type: TransactionType.BUY,
    quantity: "5",
    price: "155.00",
    total_value: "775.00",
    timestamp: "2024-02-10T15:45:00Z"
  },
  {
    id: 3,
    portfolio_id: 1,
    stock_id: 101,
    type: TransactionType.SELL,
    quantity: "4",
    price: "170.00",
    total_value: "680.00",
    timestamp: "2024-03-20T14:15:00Z"
  },
  {
    id: 4,
    portfolio_id: 1,
    stock_id: 101,
    type: TransactionType.BUY,
    quantity: "6",
    price: "165.00",
    total_value: "990.00",
    timestamp: "2024-04-18T13:55:00Z"
  },
  {
    id: 5,
    portfolio_id: 1,
    stock_id: 101,
    type: TransactionType.SELL,
    quantity: "3",
    price: "175.00",
    total_value: "525.00",
    timestamp: "2024-06-03T15:20:00Z"
  }
]
