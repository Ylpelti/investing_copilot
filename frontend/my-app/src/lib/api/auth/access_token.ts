import { cookies } from "next/headers";

export const getAccessToken = async (): Promise<string | null> => {
    const cookieStore = await cookies()
    return cookieStore.get("access_token")?.value ?? null
}