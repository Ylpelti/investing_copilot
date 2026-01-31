import { RegisterForm } from "@/components/users/registerForm"
import { createUserAction } from "@/actions/user_actions"
import Link from "next/link"

const RegisterPage = () => {
  return(
    <div>
      <RegisterForm action={createUserAction} />
      <button>
        <Link href={"/login"}>Login User</Link>
      </button>
    </div>
  ) 

}

export default RegisterPage
