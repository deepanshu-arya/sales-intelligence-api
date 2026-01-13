import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

export default function App() {
  const [data, setData] = useState([]);
  const [kpis, setKpis] = useState(null);

  // fallback data (guaranteed visible)
  const fallbackData = [
    { day: "Mon", sales: 120 },
    { day: "Tue", sales: 210 },
    { day: "Wed", sales: 150 },
    { day: "Thu", sales: 300 },
    { day: "Fri", sales: 280 },
    { day: "Sat", sales: 350 },
    { day: "Sun", sales: 400 }
  ];

  const fallbackKpis = {
  total_sales: 1810,
  average_sales: 258,
  best_day: "Sunday",
  worst_day: "Monday"
};


  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/sales/weekly")
      .then((res) => {
        if (Array.isArray(res.data) && res.data.length > 0) {
          setData(res.data);
        } else {
          setData(fallbackData);
        }
      })
      .catch(() => {
        // backend not ready → show fallback
        setData(fallbackData);
      });

    axios
  .get("http://127.0.0.1:8000/sales/kpis")
  .then(res => {
    if (res.data) {
      setKpis(res.data);
    } else {
      setKpis(fallbackKpis);
    }
  })
  .catch(() => {
    // backend not ready → show fallback KPI
    setKpis(fallbackKpis);
  });

  }, []);

  if (data.length === 0) {
    return <h2 style={{ padding: 40 }}>Loading dashboard...</h2>;
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>Sales Dashboard</h2>
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
  <div className="card">Total: ₹{kpis?.total_sales}</div>
  <div className="card">Avg: ₹{kpis?.average_sales}</div>
  <div className="card">Best: {kpis?.best_day}</div>
  <div className="card">Worst: {kpis?.worst_day}</div>
</div>


      <LineChart width={700} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="day" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="sales" stroke="#4f46e5" />
      </LineChart>
    </div>
  );
}
