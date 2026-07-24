import json
import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.graph.graph import build_graph

router = APIRouter()
graph = build_graph()


class QueryRequest(BaseModel):
    question: str
    thread_id: str | None = None


@router.post("/query")
async def query(req: QueryRequest):
    thread_id = req.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    async def event_stream():
        yield f"data: {json.dumps({'node': 'start', 'thread_id': thread_id})}\n\n"

        try:
            for event in graph.stream(
                {"question": req.question, "retry_count": 0},
                config=config,
                stream_mode="updates",
            ):
                for node_name, delta in event.items():
                    payload = {"node": node_name, "data": delta}
                    yield f"data: {json.dumps(payload, default=str)}\n\n"
        except Exception as e:
            print(f"Unhandled error in graph stream: {e}")
            error_payload = {"node": "error", "data": {"final_message": "Something went wrong processing your question. Please try again."}}
            yield f"data: {json.dumps(error_payload)}\n\n"

        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")