import { getUsers } from "@/lib/api/auth";
import { LoginForm } from "@/components/users/loginForm";
import { UserLogin } from "@/types/user";

const UsersPage = async () => {
    const handleSubmit = async (data: UserLogin) => {
        await loginUser(data)
    }
    return (
        <LoginForm onSubmit={handleSubmit} />
    )
}

export default UsersPage    