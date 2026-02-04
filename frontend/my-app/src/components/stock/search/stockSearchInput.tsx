type Props = {
    value: string
    onChange: (value: string) => void
    placeholder?: string
}

export const StockSearchInput = ({ value, onChange, placeholder = "Search stocks..."}: Props) => {

    return (
        <input type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        autoComplete="off" />
    )
}