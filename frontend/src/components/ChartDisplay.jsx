import Plot from "react-plotly.js";

function ChartDisplay({ chartSpec }) {
  if (!chartSpec || chartSpec.type === "empty") {
    return <p className="text-sm text-zinc-500 font-mono">No rows returned.</p>;
  }

  if (chartSpec.type === "table") {
    const columns = Object.keys(chartSpec.data[0] || {});
    return (
      <div className="border border-zinc-700 rounded-lg overflow-hidden">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-zinc-800">
              {columns.map((col) => (
                <th
                  key={col}
                  className="text-left px-3 py-2 font-medium text-xs uppercase tracking-wide text-zinc-400"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {chartSpec.data.map((row, i) => (
              <tr key={i} className="border-t border-zinc-800">
                {columns.map((col) => (
                  <td key={col} className="px-3 py-2 font-mono text-zinc-300">
                    {row[col]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  const xValues = chartSpec.data.map((row) => row[chartSpec.x]);
  const yValues = chartSpec.data.map((row) => row[chartSpec.y]);

  return (
    <Plot
      data={[
        {
          x: xValues,
          y: yValues,
          type: chartSpec.type === "line" ? "scatter" : "bar",
          mode: chartSpec.type === "line" ? "lines+markers" : undefined,
          marker: { color: "#fbbf24" },
          line: { color: "#fbbf24" },
        },
      ]}
      layout={{
        width: 600,
        height: 380,
        title: { text: `${chartSpec.y} by ${chartSpec.x}`, font: { color: "#e4e4e7", size: 14 } },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        font: { color: "#a1a1aa", family: "ui-monospace, monospace", size: 11 },
        margin: { t: 40, l: 50, r: 20, b: 40 },
        xaxis: { gridcolor: "#3f3f46", zerolinecolor: "#3f3f46" },
        yaxis: { gridcolor: "#3f3f46", zerolinecolor: "#3f3f46" },
      }}
      config={{ displayModeBar: false }}
    />
  );
}

export default ChartDisplay;