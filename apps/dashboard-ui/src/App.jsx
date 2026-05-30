import { useEffect, useState } from "react";
import UrlForm from "./components/UrlForm";
import UrlList from "./components/UrlList";
import Analytics from "./components/Analytics";
import { listUrls } from "./api/client";

export default function App() {
  const [urls, setUrls] = useState([]);

  useEffect(() => {
    listUrls().then(setUrls).catch(console.error);
  }, []);

  function handleShortened(result) {
    listUrls().then(setUrls).catch(console.error);
  }

  function handleDeleted(id) {
    setUrls((prev) => prev.filter((u) => u.id !== id));
  }

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "2rem" }}>
      <h1>Nimbus URL Shortener</h1>
      <UrlForm onShortened={handleShortened} />
      <h2>Your URLs</h2>
      <UrlList urls={urls} onDeleted={handleDeleted} />
      <h2>Analytics</h2>
      <Analytics urls={urls} />
    </div>
  );
}
