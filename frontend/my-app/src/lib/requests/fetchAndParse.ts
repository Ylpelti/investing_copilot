import z from "zod";

export const requestWithSchema = async <T>(
    request: () => Promise<Response>,
    schema: z.ZodType<T>) => {
        const res = await request()

        if (!res.ok) {
            throw new Error(`Request failed with: ${res.status}`)
        }
    const json = await res.json()
    return schema.parse(json)

}