import { RegisterForm } from "@/components/users/registerForm"
import { createUserAction } from "@/actions/user_actions"

const RegisterPage = () => {
  return <RegisterForm action={createUserAction} />
}

export default RegisterPage
