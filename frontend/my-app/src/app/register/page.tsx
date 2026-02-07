import { RegisterForm } from "@/components/users/registerForm"
import { createUserAction } from "@/actions/userActions"
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
