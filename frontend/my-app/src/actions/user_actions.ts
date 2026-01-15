"use server"

import { registerUser } from "@/lib/api/auth/auth"
import { loginRequest } from "@/lib/api/auth/auth"
import { cookies } from "next/headers"

export type CreateUserState = {
  success: boolean
  error?: string
}

export type LoginState = CreateUserState

export const createUserAction = async (
  prevState: CreateUserState,
  formData: FormData
): Promise<CreateUserState> => {
  try {
    const username = String(formData.get("username") ?? "").trim()
    const email = String(formData.get("email") ?? "").trim()
    const password = String(formData.get("password") ?? "").trim()

    if (!username) throw new Error("Username required")
    if (!email) throw new Error("Email required")
    if (!password) throw new Error("Password required")

    await registerUser({ username, email, password })

    return { success: true }
  } catch (e) {
    return {
      success: false,
      error: e instanceof Error ? e.message : "Unknown error",
    }
  }
}

export const loginAction = async (
  _: LoginState,
  formData:FormData
): Promise<LoginState> => {
  try {
    const username = String(formData.get("username"))
    const password = String(formData.get("password"))

    const token = await loginRequest(username, password)

    const cookieStore = await cookies()

    cookieStore.set("access_token", token.access_token, {
      httpOnly: true,
      secure: false,
      sameSite: 'lax',
      maxAge: token.expires_in,
      path: '/'
    })
    return { success: true}
  } catch(e) {
    return {
      success: false,
      error: "Invalid username or password"
    }
  }
}
