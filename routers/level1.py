from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import uuid
import json
import re
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/v1", tags=["v1"])

class TranscriptRequest(BaseModel):
    transcript: str

class ActionItem(BaseModel):
    id: str
    text: str
    status: str
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = None
    createdAt: str

class TranscriptResponse(BaseModel):
    actionItems: List[ActionItem]

# In-memory DB
action_items_db: List[ActionItem] = []


@router.get("/")
async def root_v1():
    """Root route for v1"""
    return {
        "message": "Welcome to InsightBoard AI API (Gemini) v1",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/health")
async def health_check_v1():
    """Health check for v1"""
    return {
        "status": "healthy",
        "version": "v1",
        "service": "InsightBoard Gemini API",
        "timestamp": datetime.now().isoformat(),
    }


def generate_action_items(request: Request, transcript: str) -> List[ActionItem]:
    """Generate action items using Gemini"""
    system_prompt = """You are an expert at analyzing meeting transcripts and extracting actionable tasks. 
    Always return a valid JSON array of action items with this exact structure:
    [
      {
        "text": "specific actionable task description",
        "priority": "high/medium/low",
        "tags": ["team-tag1", "team-tag2"]
      }
    ]
    Rules:
    - Extract 3-8 concrete, specific action items
    - Assign priority appropriately
    - Add relevant team tags like @Engineering, @Marketing, @Design, etc.
    - Make tasks clear, actionable, and assignable
    """

    user_prompt = f"Please analyze this meeting transcript and extract actionable tasks:\n\n{transcript}\n\nReturn ONLY the JSON array."

    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        model = request.app.state.gemini_model  # ✅ Access from app.state

        response = model.generate_content(full_prompt)
        content = response.text.strip()
        print("Raw AI Response:", content)

        # Extract JSON from Gemini output
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        json_str = json_match.group() if json_match else content
        items_data = json.loads(json_str)

        action_items = [
            ActionItem(
                id=str(uuid.uuid4()),
                text=item["text"],
                status="pending",
                priority=item.get("priority", "medium"),
                tags=item.get("tags", ["General"]),
                createdAt=datetime.now().isoformat()
            )
            for item in items_data
        ]
        return action_items

    except Exception as e:
        print(f"Error generating action items: {e}")
        return []


@router.get("/transcript")
async def get_transcript():
    return {
        "status": "success",
        "message": "Transcript endpoint is active and ready",
        "timestamp": datetime.now().isoformat()
    }


@router.post("/transcript", response_model=TranscriptResponse)
async def process_transcript(request: Request, body: TranscriptRequest):
    """Process transcript and generate action items"""
    try:
        if not body.transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript cannot be empty")

        action_items = generate_action_items(request, body.transcript)
        action_items_db.extend(action_items)

        return TranscriptResponse(actionItems=action_items)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing transcript: {str(e)}")


@router.get("/action-items", response_model=List[ActionItem])
async def get_action_items():
    """Get all action items"""
    return action_items_db


@router.put("/action-items/{item_id}")
async def update_action_item(item_id: str, updates: dict):
    """Update action item (status, priority, etc.)"""
    for item in action_items_db:
        if item.id == item_id:
            for key, value in updates.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            return item
    raise HTTPException(status_code=404, detail="Action item not found")


@router.delete("/action-items/{item_id}")
async def delete_action_item(item_id: str):
    """Delete action item"""
    global action_items_db
    before = len(action_items_db)
    action_items_db = [item for item in action_items_db if item.id != item_id]

    if len(action_items_db) == before:
        raise HTTPException(status_code=404, detail="Action item not found")

    return {"message": f"Action item {item_id} deleted successfully"}
