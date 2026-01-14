// src/lib/mocks/positionMockData.ts
import { PortfolioRead } from "@/types/portfolio";
import { PositionRead, PositionCreate } from "@/types/position";

let nextId = 6

export let mockPositions: PositionRead[] = [
  {
    id: 1,
    portfolio_id: 1,
    stock_id: 101,
    symbol: "AAPL",
    quantity: 15,
    buy_price: 145.20,
  },
  {
    id: 2,
    portfolio_id: 1,
    stock_id: 102,
    symbol: "MSFT",
    quantity: 8,
    buy_price: 312.50,
  },
  {
    id: 3,
    portfolio_id: 1,
    stock_id: 103,
    symbol: "GOOGL",
    quantity: 5,
    buy_price: 2710.00,
  },
  {
    id: 4,
    portfolio_id: 2,
    stock_id: 201,
    symbol: "TSLA",
    quantity: 12,
    buy_price: 215.40,
  },
  {
    id: 5,
    portfolio_id: 2,
    stock_id: 202,
    symbol: "NVDA",
    quantity: 6,
    buy_price: 495.10,
  },
];

export const createMockPosition = (data: PositionCreate): PositionRead => {
  if (!data) {
    throw new Error("Data missing")
  }
  const newPosition:PositionRead = {
    id: nextId++,
    symbol: data.symbol,
    quantity: data.quantity,
    portfolio_id: data.portfolio_id,
    stock_id: data.stock_id,
    buy_price: data.buy_price
  }
  mockPositions = [...mockPositions, newPosition]

  return newPosition
}