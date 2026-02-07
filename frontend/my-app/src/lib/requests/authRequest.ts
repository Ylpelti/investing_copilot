const API_BASE = process.env.NEXT_PUBLIC_API_URL!;

import { getAccessToken } from "../api/auth/access_token"

export const authRequest = async <T>(path: string, init?: RequestInit) => {
    const token = await getAccessToken()
    if (!token) {
        throw new Error("No access")
    }
    const res = await fetch(`${API_BASE}${path}`, {
        ...init,
        credentials: "include",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-type": "application/json",
            ...(init?.headers ?? {})
        },
        cache: "no-store"
    })

    if (!res.ok) {
        const text = await res.text().catch(() => "")
        throw new Error(`Request faile (${res.status}: ${text})`)
    }

    return (await res.json()) as T
}