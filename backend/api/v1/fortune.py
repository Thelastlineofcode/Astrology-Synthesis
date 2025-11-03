"""Fortune reading API endpoints for Mula: The Root."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import random

router = APIRouter(prefix="/fortune", tags=["fortune"])


class Card(BaseModel):
    """Vodou Oracle card model."""
    id: str
    name: str
    subtitle: str
    symbol: str
    meaning: str
    advice: str
    element: Optional[str] = None
    planet: Optional[str] = None


class FortuneRequest(BaseModel):
    """Request for fortune reading."""
    reading_type: str = Field(..., description="Type: 'daily', 'weekly', 'monthly', 'custom'")
    question: Optional[str] = Field(None, description="User's specific question (for custom readings)")
    user_context: Optional[dict] = Field(None, description="User's natal chart and profile")


class FortuneResponse(BaseModel):
    """Response with fortune reading."""
    reading_type: str
    card: Card
    interpretation: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Vodou Oracle cards
ORACLE_CARDS = [
    Card(
        id="papa-legba",
        name="Papa Legba",
        subtitle="The Crossroads",
        symbol="🗝️",
        meaning="Papa Legba stands at the crossroads of destiny. New opportunities await you, but decisive action is required.",
        advice="Open doors are meant to be walked through. Trust your intuition and take the first step into the unknown.",
        element="Air",
        planet="Mercury"
    ),
    Card(
        id="erzulie-freda",
        name="Erzulie Freda",
        subtitle="Love & Beauty",
        symbol="💝",
        meaning="The Lwa of love and beauty blesses your path. Emotional fulfillment and deep connections are approaching.",
        advice="Open your heart to receive love. Self-care and appreciation of beauty will attract positive energy.",
        element="Water",
        planet="Venus"
    ),
    Card(
        id="baron-samedi",
        name="Baron Samedi",
        subtitle="Death & Rebirth",
        symbol="💀",
        meaning="The Baron teaches that endings are new beginnings. A transformation is underway in your life.",
        advice="Release what no longer serves you. Embrace change fearlessly, for rebirth follows death.",
        element="Earth",
        planet="Pluto"
    ),
    Card(
        id="ogoun",
        name="Ogoun",
        subtitle="Strength & War",
        symbol="⚔️",
        meaning="Ogoun brings the fire of determination. Your strength and courage will overcome obstacles.",
        advice="Stand firm in your convictions. Victory comes to those who fight with honor and persistence.",
        element="Fire",
        planet="Mars"
    ),
    Card(
        id="damballah",
        name="Damballah",
        subtitle="Wisdom & Purity",
        symbol="🐍",
        meaning="The Serpent Lwa offers ancient wisdom and spiritual clarity. Truth is revealing itself to you.",
        advice="Seek inner peace through meditation and reflection. Wisdom comes from stillness.",
        element="Ether",
        planet="Jupiter"
    ),
    Card(
        id="ayizan",
        name="Ayizan",
        subtitle="The Priestess",
        symbol="🌿",
        meaning="Ayizan guards spiritual knowledge and ancestral wisdom. Divine feminine power awakens within you.",
        advice="Trust your intuition and spiritual practices. Connect with your ancestors for guidance.",
        element="Earth",
        planet="Moon"
    ),
    Card(
        id="agwe",
        name="Agwe",
        subtitle="Lord of the Sea",
        symbol="🌊",
        meaning="Agwe rules the ocean's depths. Emotional currents and hidden treasures emerge to the surface.",
        advice="Go with the flow but stay anchored. Deep emotions need acknowledgment, not suppression.",
        element="Water",
        planet="Neptune"
    ),
    Card(
        id="simbi",
        name="Simbi",
        subtitle="The Sorcerer",
        symbol="🐸",
        meaning="Simbi brings magic and transformation. Your creative power manifests through focused intention.",
        advice="Harness your will to create change. Magic is simply focused consciousness in action.",
        element="Water",
        planet="Uranus"
    )
]


@router.post("/draw", response_model=FortuneResponse)
async def draw_fortune(request: FortuneRequest):
    """
    Draw a fortune card and receive interpretation.
    
    Reading types:
    - daily: Quick guidance for the day
    - weekly: Overview for the week ahead
    - monthly: Month-long forecast
    - custom: Answer to specific question
    """
    # Validate reading type
    valid_types = ["daily", "weekly", "monthly", "custom"]
    if request.reading_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid reading_type. Must be one of: {', '.join(valid_types)}"
        )
    
    # Custom readings require a question
    if request.reading_type == "custom" and not request.question:
        raise HTTPException(
            status_code=400,
            detail="Custom readings require a 'question' field"
        )
    
    # Draw random card
    card = random.choice(ORACLE_CARDS)
    
    # Generate interpretation based on reading type
    interpretation = generate_interpretation(request.reading_type, card, request.question)
    
    return FortuneResponse(
        reading_type=request.reading_type,
        card=card,
        interpretation=interpretation
    )


@router.get("/cards", response_model=List[Card])
async def list_cards():
    """Get list of all Vodou Oracle cards."""
    return ORACLE_CARDS


@router.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: str):
    """Get details about a specific card."""
    card = next((c for c in ORACLE_CARDS if c.id == card_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


def generate_interpretation(reading_type: str, card: Card, question: Optional[str] = None) -> str:
    """Generate contextual interpretation based on reading type."""
    
    if reading_type == "daily":
        return f"Today, {card.name} appears to guide your path. {card.meaning} Focus on the message: {card.advice}"
    
    elif reading_type == "weekly":
        return f"This week is influenced by {card.name}. {card.meaning} Throughout the next seven days: {card.advice}"
    
    elif reading_type == "monthly":
        return f"The month ahead carries the energy of {card.name}. {card.meaning} Over the coming weeks: {card.advice}"
    
    elif reading_type == "custom" and question:
        return f"In response to your question '{question}', {card.name} appears. {card.meaning} Guidance: {card.advice}"
    
    return f"{card.name} brings this message: {card.meaning} {card.advice}"


# TODO: Backend implementation tasks
# 1. Store readings in database (readings table)
# 2. Add user authentication and reading history
# 3. Implement daily reading limits (1 free daily, premium unlimited)
# 4. Add AI-enhanced interpretations using LLM + user natal chart
# 5. Create multi-card spreads (3-card, Celtic Cross)
# 6. Add Tarot deck support (Rider-Waite, Lenormand)
# 7. Implement card reversal logic (upright vs reversed meanings)
