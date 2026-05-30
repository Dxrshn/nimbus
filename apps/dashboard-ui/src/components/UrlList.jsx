import { deleteUrl } from "../api/client";

export default function UrlList({ urls, onDeleted }) {
  async function handleDelete(id) {
    try {
      await deleteUrl(id);
      onDeleted(id);
    } catch {
      alert("Failed to delete URL");
    }
  }

  if (urls.length === 0) return <p>No URLs yet. Shorten one above.</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Short URL</th>
          <th>Original</th>
          <th>Clicks</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {urls.map((u) => (
          <tr key={u.id}>
            <td>
              <a href={u.short_url} target="_blank" rel="noreferrer">
                {u.short_url}
              </a>
            </td>
            <td>{u.original_url}</td>
            <td>{u.click_count}</td>
            <td>
              <button onClick={() => handleDelete(u.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
