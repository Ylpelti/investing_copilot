import { UserRead } from "@/types/user";

export const UserList = ({ users } : {users: UserRead[]}) => {
    return (
        <ul>
            {users.map(u => (
                <li key={u.id}>{u.username}</li>
            ))}
        </ul>
    )
}