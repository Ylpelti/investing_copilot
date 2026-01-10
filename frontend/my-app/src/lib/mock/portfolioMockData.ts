import { PortfolioRead } from "@/types/portfolio";

export let mockPortfolios: PortfolioRead[] = [
  {
    id: 1,
    user_id: 42,
    name: "Long-Term Investments",
    description: "Buy and hold strategy for retirement",
    created_at: "2024-01-10T09:15:00Z",
    updated_at: "2024-02-01T14:20:00Z",
  },
  {
    id: 2,
    user_id: 42,
    name: "Tech Growth",
    description: null,
    created_at: "2024-03-05T11:45:00Z",
    updated_at: "2024-03-20T08:30:00Z",
  },
  {
    id: 3,
    user_id: 42,
    name: "Dividend Income",
    description: "Focus on stable dividend-paying stocks",
    created_at: "2024-04-01T16:00:00Z",
    updated_at: "2024-04-15T10:10:00Z",
  },
]; 

export function setMockPortfolios(next: PortfolioRead[]) {
  mockPortfolios = next;
}