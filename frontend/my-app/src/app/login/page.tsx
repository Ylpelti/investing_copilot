"use server"
import { LoginForm } from "@/components/users/loginForm";
import { loginAction } from "@/actions/user_actions";


const UsersPage = async () => {

    return (
        <LoginForm action={loginAction} />
    )
}

export default UsersPage    