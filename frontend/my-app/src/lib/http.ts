const API_BASE = process.env.NEXT_PUBLIC_API_URL!;
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true";

export function usingMock() {
  return USE_MOCK;
}

export const request = async <T>(path: string, init?: RequestInit): Promise<T> => {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Request failed (${res.status}): ${text || res.statusText}`);
  }

  return (await res.json()) as T;
}
