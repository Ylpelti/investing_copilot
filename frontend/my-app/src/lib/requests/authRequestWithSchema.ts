import { getAccessToken } from "../api/auth/access_token"
const API_BASE = process.env.NEXT_PUBLIC_API_URL!;

export const authRequestWithSchema = async (
    path:string,
    init?: RequestInit ) => {
        const token = await getAccessToken()
        if (!token) throw new Error("No access")
        return await fetch(`${API_BASE}${path}`, {
        ...init,
        credentials: "include",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-type": "application/json",
            ...(init?.headers ?? {})
        },
        cache: "no-store"
    })
}