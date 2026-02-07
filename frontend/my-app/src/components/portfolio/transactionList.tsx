import { TransactionRead } from "@/types/transaction";

export const TransactionList = ({ transactions }: {transactions: TransactionRead[]}) => {
    return (
        <ul>
            {transactions.map(t => (
                <li key={t.id}>
                {t.quantity}
                {t.total_value}</li>
            ))}
        </ul>
    )
}