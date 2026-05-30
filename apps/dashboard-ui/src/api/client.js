const BASE_URL = import.meta.env.VITE_API_URL || "";

export async function shortenUrl(url) {
  const res = await fetch(`${BASE_URL}/api/v1/shorten`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error("Failed to shorten URL");
  return res.json();
}

export async function listUrls() {
  const res = await fetch(`${BASE_URL}/api/v1/urls`);
  if (!res.ok) throw new Error("Failed to fetch URLs");
  return res.json();
}

export async function deleteUrl(id) {
  const res = await fetch(`${BASE_URL}/api/v1/urls/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete URL");
}
