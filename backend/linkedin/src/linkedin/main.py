#!/usr/bin/env python
import os
import sys
from datetime import datetime
import logging
from fastapi import Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ─── 1) Make sure Python can see both 'linkedin/' and 'tools/' ────────────────
# Current file is src/linkedin/main.py, so src/ is two levels up:
SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, SRC_ROOT)

# ─── 2) Now these imports will work ────────────────────────────────────────────
from linkedin.crew import LinkedInPoster
from tools.linkedin_publish import linkedin_publish
from tools.linkedin_metrics import linkedin_metrics

# ─── 3) Load .env and configure logging ───────────────────────────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO)
logging.info("Starting FastAPI LinkedInPoster service")

# ─── 4) Instantiate FastAPI and enable CORS ──────────────────────────────────
app = FastAPI(title="LinkedIn AI Poster API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your UI origin
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ─── 5) Create the Crew once ─────────────────────────────────────────────────
try:
    poster_crew = LinkedInPoster().crew()
    logging.info("✅ Crew loaded successfully")
except Exception as e:
    logging.exception("❌ Crew initialization failed")
    raise

# ─── 6) Request/body models ──────────────────────────────────────────────────
class TopicRequest(BaseModel):
    topic: str

class PublishRequest(BaseModel):
    draft: str

# ─── 7) Health check ─────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "OK", "time": datetime.utcnow().isoformat()}

# ─── 8) Generate draft ────────────────────────────────────────────────────────
@app.post("/generate")
async def generate(request: Request):
    payload = await request.json()
    topic = payload.get("topic")
    if not topic:
        raise HTTPException(status_code=400, detail="Missing 'topic'")

    logging.info(f"→ /generate topic={topic}")
    try:
        results = poster_crew.kickoff(
            inputs={
                "topic": topic,
                "current_year": str(datetime.utcnow().year)
            }
        )

        # Extract the list of TaskOutput objects
        task_outputs = getattr(results, "tasks_output", None)
        if not task_outputs:
            raise RuntimeError("No tasks_output found on CrewOutput")

        # Pull out the write_task raw text
        draft = next(
            (to.raw for to in task_outputs if to.name == "write_task"),
            None
        )
        if draft is None:
            raise RuntimeError(
                f"write_task output not found; saw tasks: {[to.name for to in task_outputs]}"
            )

        return {"draft": draft}

    except Exception as e:
        logging.exception("Error in /generate")
        raise HTTPException(status_code=500, detail=str(e))


# ─── 9) Publish to LinkedIn ───────────────────────────────────────────────────
@app.post("/publish")
def publish(req: PublishRequest):
    logging.info(f"→ /publish draft_length={len(req.draft)}")
    try:
        url = linkedin_publish(req.draft)
        if url.startswith("Error"):
            logging.error("LinkedIn publish error: %s", url)
            raise HTTPException(status_code=500, detail=url)
        return {"url": url}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error in /publish")
        raise HTTPException(status_code=500, detail=str(e))

# ─── 10) Fetch metrics ────────────────────────────────────────────────────────
@app.get("/metrics/{post_urn}")
def metrics(post_urn: str):
    logging.info(f"→ /metrics urn={post_urn}")
    try:
        data = linkedin_metrics(post_urn)
        return data
    except Exception as e:
        logging.exception("Error in /metrics")
        raise HTTPException(status_code=500, detail=str(e))
