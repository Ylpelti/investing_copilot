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
            <td>{p.quantity}</td>
            <td>{p.buy_price}</td>
          </tr>
        ))}
      </tbody>
    </table>
    )
}