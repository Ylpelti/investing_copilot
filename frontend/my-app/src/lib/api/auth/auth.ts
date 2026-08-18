import { UserRead, UserCreate } from "@/types/user";
import { apiRequest } from "../../requests/http";
import { authRequest } from "@/lib/requests/authRequest";

export const registerUser = async (data: UserCreate): Promise<UserRead> => {
    

    return apiRequest<UserRead>("/users", {
        method: "POST",
        body: JSON.stringify(data),
    })
}

export const loginRequest = async (username:string, password:string) => {
    const body = new URLSearchParams()
    body.set("username", username)
    body.set("password", password)

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded",
    },
    body
})
    if (!res.ok) {
        throw new Error("Wrong username or password")
    }

    return res.json() as Promise<{
        access_token: string
        token_type: "bearer"
        expires_in: number
    }>
}

export const getCurrentUser = async () => {
    return authRequest<UserRead>("/users/me", {
        method: "GET",
    })
}
