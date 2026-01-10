import { PositionRead } from "@/types/position"

export const PositionTable = async ({ positions }: {positions: PositionRead[]}) => {
    return (
        <div>
          {positions.map(p => (
            <p key={p.id}> 
              {p.symbol}
              {p.quantity}
              {p.stock_id} 
            </p>
          ))}
        </div>
    )
}