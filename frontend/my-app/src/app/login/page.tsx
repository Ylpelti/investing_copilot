"use server"
import { LoginForm } from "@/components/users/loginForm";
import { loginAction } from "@/actions/user_actions";
import Link from "next/link";


const UsersPage = async () => {

    return (
        <div>
        <LoginForm action={loginAction} />
        <button>
        <Link href={"/register"}>Register new user</Link>
        <Link href={"/me"}>To me page</Link>
        </button>
        </div>
    )
}

export default UsersPage    