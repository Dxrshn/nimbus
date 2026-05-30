import { useState } from "react";
import { shortenUrl } from "../api/client";

export default function UrlForm({ onShortened }) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await shortenUrl(url);
      setUrl("");
      onShortened(result);
    } catch {
      setError("Failed to shorten URL. Make sure it starts with https://");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://example.com"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Shortening..." : "Shorten"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
