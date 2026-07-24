import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export async function streamQuery(question, threadId, onEvent) {
  let lastLength = 0;
  let buffer = "";

  await axios.post(
    API_URL,
    { question, thread_id: threadId },
    {
      responseType: "text",
      onDownloadProgress: (progressEvent) => {
        const fullText = progressEvent.event.target.responseText;
        const newChunk = fullText.slice(lastLength);
        lastLength = fullText.length;

        buffer += newChunk;
        const parts = buffer.split("\n\n");
        buffer = parts.pop();

        for (const part of parts) {
          if (!part.startsWith("data: ")) continue;
          const raw = part.slice(6).trim();
          if (raw === "[DONE]") continue;
          onEvent(JSON.parse(raw));
        }
      },
    }
  );
}