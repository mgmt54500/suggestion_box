from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import bigquery
from pydantic import BaseModel

# ── Configuration ──────────────────────────────────────────────────────────────
# Replace these two values with your actual GCP project ID and dataset name
# before running the app.
PROJECT_ID = "your-project-id"
DATASET_ID = "suggestion_box"

TABLE = f"{PROJECT_ID}.{DATASET_ID}.suggestions"

# ── BigQuery client ────────────────────────────────────────────────────────────
client = bigquery.Client(project=PROJECT_ID)

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI()

# CORS middleware tells the browser which cross-origin requests are allowed.
# Allowing all origins ("*") is fine for a classroom demo but should be
# restricted to specific domains in a real production application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # accept requests from any origin
    allow_methods=["GET", "POST"],
    allow_headers=["*"],       # accept any request headers
)


# ── Pydantic model ─────────────────────────────────────────────────────────────
# Pydantic validates incoming JSON automatically. If a request body is missing
# a required field or has the wrong type, FastAPI returns a 422 error before
# our code ever runs.
#
# Literal restricts `category` to exactly three allowed string values; any
# other value is rejected at validation time.
class SuggestionCreate(BaseModel):
    category: Literal["Facilities", "Technology", "General"]
    message: str


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/suggestions")
def list_suggestions():
    """Return all suggestions, newest first."""
    query = f"""
        SELECT id, category, message, created_at
        FROM `{TABLE}`
        ORDER BY created_at DESC
    """
    rows = client.query(query).result()
    return [dict(row) for row in rows]


@app.get("/suggestions/{id}")
def get_suggestion(id: str):
    """Return a single suggestion by ID, or 404 if not found."""
    query = f"""
        SELECT id, category, message, created_at
        FROM `{TABLE}`
        WHERE id = {id}
        LIMIT 1
    """
    rows = list(client.query(query).result())
    if not rows:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return dict(rows[0])


@app.post("/suggestions", status_code=201)
def create_suggestion(body: SuggestionCreate):
    """Insert a new suggestion and return the created record."""
    # Generate a unique id using BigQuery's built-in GENERATE_UUID().
    insert_query = f"""
        INSERT INTO `{TABLE}` (id, category, message, created_at)
        VALUES (
            GENERATE_UUID(),
            '{body.category}',
            '''{body.message}''',
            CURRENT_TIMESTAMP()
        )
    """
    client.query(insert_query).result()

    # Fetch and return the row we just inserted.
    fetch_query = f"""
        SELECT id, category, message, created_at
        FROM `{TABLE}`
        ORDER BY created_at DESC
        LIMIT 1
    """
    rows = list(client.query(fetch_query).result())
    return dict(rows[0])
