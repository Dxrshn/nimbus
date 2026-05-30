import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Analytics({ urls }) {
  const data = urls
    .filter((u) => u.click_count > 0)
    .map((u) => ({
      name: u.short_url.split("/").pop(),
      clicks: u.click_count,
    }));

  if (data.length === 0) return <p>No click data yet.</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="clicks" fill="#646cff" />
      </BarChart>
    </ResponsiveContainer>
  );
}
