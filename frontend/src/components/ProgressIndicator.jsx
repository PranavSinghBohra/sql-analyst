const LABELS = {
  generate_sql: "Generating SQL",
  validate_and_execute: "Running query",
  reflect: "Query failed — rewriting",
  generate_chart: "Building chart",
  generate_insight: "Summarizing results",
  give_up: "Could not complete the query",
};

const DOT_STYLES = {
  generate_sql: "bg-emerald-400",
  validate_and_execute: "bg-emerald-400",
  reflect: "bg-amber-400",
  generate_chart: "bg-emerald-400",
  generate_insight: "bg-emerald-400",
  give_up: "bg-red-400",
};

function ProgressIndicator({ steps, loading }) {
  return (
    <ul className="relative">
      {steps.map((step, i) => (
        <li key={i} className="flex items-center gap-3 py-1.5 relative">
          {i < steps.length - 1 && (
            <span className="absolute left-1.25 top-6 w-px h-full bg-zinc-700" />
          )}
          <span
            className={`w-2.75 h-2.75 rounded-full shrink-0 ${
              DOT_STYLES[step] || "bg-zinc-500"
            }`}
          />
          <span className="text-sm text-zinc-400 font-mono">
            {LABELS[step] || step}
          </span>
        </li>
      ))}
      {loading && (
        <li className="flex items-center gap-3 py-1.5">
          <span className="w-2.75 h-2.75\ rounded-full bg-amber-400 animate-pulse shrink-0" />
          <span className="text-sm text-zinc-500 font-mono">Working...</span>
        </li>
      )}
    </ul>
  );
}

export default ProgressIndicator;