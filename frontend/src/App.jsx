import { useState } from "react";
import { streamQuery } from "./api/queryStream";
import ChatInput from "./components/ChatInput";
import ProgressIndicator from "./components/ProgressIndicator";
import ChartDisplay from "./components/ChartDisplay";

function App() {
  const [threadId, setThreadId] = useState(null);
  const [steps, setSteps] = useState([]);
  const [sqlQuery, setSqlQuery] = useState(null);
  const [chartSpec, setChartSpec] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [insight, setInsight] = useState(null);

  const handleAsk = async (question) => {
    setSteps([]);
    setSqlQuery(null);
    setChartSpec(null);
    setErrorMessage(null);
    setLoading(true);
    setInsight(null);

    try {
      await streamQuery(question, threadId, (event) => {
        if (event.node === "start") {
          setThreadId(event.thread_id);
          return;
        }

        setSteps((prev) => [...prev, event.node]);

        if (event.data?.sql_query) {
          setSqlQuery(event.data.sql_query);
        }
        if (event.data?.chart_spec) {
          setChartSpec(event.data.chart_spec);
        }
        if (event.data?.final_message) {
          setErrorMessage(event.data.final_message);
        }
        if (event.data?.insight) {
          setInsight(event.data.insight);
        }
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-900 text-zinc-100">
      <div className="max-w-2xl mx-auto pt-16 px-4 pb-16">
        <div className="mb-8">
          <h1 className="text-lg font-mono text-zinc-100">
            <span className="text-amber-400">&gt;</span> sql-analyst
          </h1>
          <p className="text-sm text-zinc-500 mt-1">
            Ask questions about your data in plain English.
          </p>
        </div>

        <div className="bg-zinc-800/40 border border-zinc-700 rounded-xl p-5">
          <ChatInput onSubmit={handleAsk} disabled={loading}/>

          {steps.length > 0 && (
            <div className="mt-5 pt-5 border-t border-zinc-800">
              <ProgressIndicator steps={steps} loading={loading} />
            </div>
          )}

          {sqlQuery && (
            <pre className="mt-5 bg-zinc-950 border border-zinc-800 rounded-lg p-3.5 text-xs text-zinc-300 font-mono overflow-x-auto">
              {sqlQuery}
            </pre>
          )}

          {errorMessage && (
            <p className="mt-5 text-sm text-red-400 font-mono">{errorMessage}</p>
          )}

          {insight && (
            <p className="mt-5 text-sm text-zinc-300 font-mono">{insight}</p>
          )}

          {chartSpec && (
            <div className="mt-5 flex justify-center">
              <ChartDisplay chartSpec={chartSpec} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;