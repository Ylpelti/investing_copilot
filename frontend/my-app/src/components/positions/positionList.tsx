import { PositionRead } from "@/types/position"

export const PositionTable = async ({ positions }: {positions: PositionRead[]}) => {
    return (
        <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Quantity</th>
          <th>Buy price</th>
        </tr>
      </thead>
      <tbody>
        {positions.map((p) => (
          <tr key={p.id}>
            <td>{p.symbol}</td>
            <td>{Number(p.quantity).toFixed(1)}</td>
            <td>{Number(p.buy_price).toFixed(2)}</td>
            
          </tr>
        ))}
      </tbody>
    </table>
    )
}