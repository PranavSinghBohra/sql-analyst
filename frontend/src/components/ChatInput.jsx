import { useState } from "react";

function ChatInput({ onSubmit, disabled }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || disabled) return;
    onSubmit(question);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about the data..."
        disabled={disabled}
        className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-3.5 py-2.5 text-sm text-zinc-100 placeholder-zinc-500 outline-none focus:border-amber-400/60 focus:ring-1 focus:ring-amber-400/40 disabled:opacity-50 transition-colors"
      />
      <button
        type="submit"
        disabled={disabled}
        className="bg-amber-400 text-zinc-900 font-medium rounded-lg px-4 py-2.5 text-sm hover:bg-amber-300 disabled:opacity-40 disabled:hover:bg-amber-400 cursor-pointer disabled:cursor-not-allowed transition-colors"
        >
        Ask
      </button>
    </form>
  );
}

export default ChatInput;