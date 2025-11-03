"""Consultant chat API endpoints for Mula: The Root."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import random

router = APIRouter(prefix="/consultant", tags=["consultant"])


class Message(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request to send a message to consultant."""
    advisor_id: str = Field(..., description="ID of Lwa advisor: papa-legba, erzulie-freda, baron-samedi, ogoun")
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    chat_history: Optional[List[Message]] = Field(default=[], description="Previous conversation history")
    user_context: Optional[dict] = Field(default=None, description="User's natal chart and profile data")


class ChatResponse(BaseModel):
    """Response from consultant chat."""
    advisor_id: str
    advisor_name: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    suggestions: Optional[List[str]] = Field(default=None, description="Follow-up suggestions")


class Advisor(BaseModel):
    """Lwa advisor persona."""
    id: str
    name: str
    title: str
    symbol: str
    description: str
    color: str
    domains: List[str]


# Advisor personas with enhanced metadata
ADVISORS = {
    "papa-legba": Advisor(
        id="papa-legba",
        name="Papa Legba",
        title="The Gatekeeper",
        symbol="🗝️",
        description="Guardian of crossroads, opener of doors, facilitator of communication",
        color="#E8B598",
        domains=["crossroads", "decisions", "opportunities", "communication", "gates", "beginnings"]
    ),
    "erzulie-freda": Advisor(
        id="erzulie-freda",
        name="Erzulie Freda",
        title="Goddess of Love",
        symbol="💝",
        description="Spirit of love, beauty, luxury, and emotional healing",
        color="#E86F4D",
        domains=["love", "relationships", "beauty", "self-care", "emotions", "healing", "romance"]
    ),
    "baron-samedi": Advisor(
        id="baron-samedi",
        name="Baron Samedi",
        title="Lord of Death",
        symbol="💀",
        description="Master of death and rebirth, guardian of cemeteries, bringer of dark wisdom",
        color="#8B6FA8",
        domains=["transformation", "endings", "shadow work", "death", "rebirth", "humor", "acceptance"]
    ),
    "ogoun": Advisor(
        id="ogoun",
        name="Ogoun",
        title="Warrior Spirit",
        symbol="⚔️",
        description="Fierce warrior, patron of iron and fire, defender of justice",
        color="#5FA9B8",
        domains=["strength", "career", "conflict", "victory", "courage", "discipline", "protection"]
    )
}


# Response templates by advisor (to be replaced with LLM)
RESPONSE_TEMPLATES = {
    "papa-legba": [
        "The crossroads before you hold many possibilities. Trust your intuition to choose the path that calls to your spirit.",
        "New opportunities are opening, but you must first close the door on what no longer serves you.",
        "Every ending is a new beginning. I open the gate—will you walk through?",
        "Communication is key. Speak your truth clearly, and doors will open before you.",
        "The path you seek is already beneath your feet. You need only trust where it leads."
    ],
    "erzulie-freda": [
        "Self-love is the foundation of all other love. Honor yourself first, and others will follow.",
        "Beauty is not just what you see, but what you feel within. Nurture your inner radiance.",
        "Love requires both strength and softness. Open your heart while keeping your boundaries clear.",
        "Treat yourself with the tenderness you offer others. You deserve the same care.",
        "Your heart is precious—protect it, but do not let fear close it to connection."
    ],
    "baron-samedi": [
        "What you fear most is often what you need to embrace. Dance with your shadows.",
        "Death clears the way for rebirth. Release what weighs you down, and rise renewed.",
        "Humor is the medicine for the soul. Do not take yourself too seriously in this game of life.",
        "Every ending teaches a lesson. What are you ready to let die?",
        "The grave holds no power over those who truly live. Embrace your mortality and thrive."
    ],
    "ogoun": [
        "Victory comes to those who stand firm. Do not retreat from the battle that shapes you.",
        "Your strength is greater than you know. Channel your fire with purpose and discipline.",
        "Conflict is not your enemy—it is your teacher. Learn what it has to show you.",
        "Cut through obstacles with precision. The warrior's sword is both weapon and tool.",
        "Courage is not the absence of fear, but action despite it. Step forward, warrior."
    ]
}


@router.post("/chat", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the spiritual consultant and receive guidance.
    
    Currently returns simulated responses. Will be enhanced with:
    - LLM integration (GPT-4 with advisor persona prompts)
    - RAG pipeline (knowledge base retrieval)
    - User context awareness (natal chart, previous readings)
    - Chat history storage in database
    """
    # Validate advisor
    if request.advisor_id not in ADVISORS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid advisor_id. Must be one of: {', '.join(ADVISORS.keys())}"
        )
    
    advisor = ADVISORS[request.advisor_id]
    
    # Get simulated response (will be replaced with LLM call)
    templates = RESPONSE_TEMPLATES[request.advisor_id]
    response_text = random.choice(templates)
    
    # Generate follow-up suggestions
    suggestions = generate_suggestions(request.advisor_id, request.message)
    
    return ChatResponse(
        advisor_id=advisor.id,
        advisor_name=advisor.name,
        response=response_text,
        suggestions=suggestions
    )


@router.get("/advisors", response_model=List[Advisor])
async def list_advisors():
    """Get list of all available Lwa advisors."""
    return list(ADVISORS.values())


@router.get("/advisors/{advisor_id}", response_model=Advisor)
async def get_advisor(advisor_id: str):
    """Get details about a specific advisor."""
    if advisor_id not in ADVISORS:
        raise HTTPException(status_code=404, detail="Advisor not found")
    return ADVISORS[advisor_id]


def generate_suggestions(advisor_id: str, user_message: str) -> List[str]:
    """Generate contextual follow-up suggestions based on advisor and message."""
    suggestions_by_advisor = {
        "papa-legba": [
            "What doors are you ready to open?",
            "Tell me about a crossroads you face.",
            "Draw a card for guidance."
        ],
        "erzulie-freda": [
            "How can you show yourself more love today?",
            "What relationships need attention?",
            "Explore your heart's desires."
        ],
        "baron-samedi": [
            "What are you ready to release?",
            "Tell me about a transformation you seek.",
            "Draw a death/rebirth card."
        ],
        "ogoun": [
            "What battle are you fighting?",
            "Where do you need more courage?",
            "Get career guidance."
        ]
    }
    
    return suggestions_by_advisor.get(advisor_id, [])


# TODO: Backend implementation tasks
# 1. Integrate OpenAI GPT-4 with advisor-specific system prompts
# 2. Add RAG pipeline: retrieve relevant texts from knowledge base
# 3. Include user natal chart context in prompts
# 4. Store chat history in PostgreSQL (consultant_messages table)
# 5. Add rate limiting (e.g., 20 messages per day for free users)
# 6. Implement premium features: voice input/output, unlimited messages
# 7. Add sentiment analysis to detect when to suggest professional help
