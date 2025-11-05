"""
Advisor (AI personality) endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.database import User, Advisor, Message, BirthChart
from app.schemas.models import AdvisorResponse, AdvisorQuery, MessageResponse

router = APIRouter()


@router.get("/list", response_model=list[AdvisorResponse])
async def list_advisors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all available advisors.
    
    - Returns Papa Legba, Marie Laveau, etc.
    - Includes personality info and avatars
    """
    advisors = db.query(Advisor).filter(Advisor.is_active == True).all()
    
    # If no advisors exist, create default ones
    if not advisors:
        default_advisors = [
            Advisor(
                name="Papa Legba",
                title="Guardian of Crossroads",
                personality_type="guidance",
                system_prompt="You are Papa Legba, guardian of crossroads and gatekeeper between worlds. You speak with wisdom about life paths, decisions, and timing. Reference Vedic astrology concepts when appropriate.",
                description="Papa Legba opens doors and reveals paths. Consult him for guidance on major life decisions and understanding your current dasha period.",
                is_active=True
            ),
            Advisor(
                name="Marie Laveau",
                title="Vodou Queen",
                personality_type="healing",
                system_prompt="You are Marie Laveau, powerful healer and spiritual practitioner. You offer wisdom on emotional healing, relationships, and spiritual protection.",
                description="Marie Laveau brings healing and spiritual insight. Ask her about emotional matters, relationships, and spiritual growth.",
                is_active=True
            ),
            Advisor(
                name="Erzulie Dantor",
                title="Fierce Protector",
                personality_type="protection",
                system_prompt="You are Erzulie Dantor, fierce protector of women and children. You speak directly about boundaries, strength, and standing your ground.",
                description="Erzulie Dantor protects and empowers. Consult her about setting boundaries, finding strength, and protecting what matters.",
                is_active=True
            )
        ]
        
        for advisor in default_advisors:
            db.add(advisor)
        db.commit()
        
        advisors = default_advisors
    
    return advisors


@router.post("/query", response_model=MessageResponse)
async def query_advisor(
    query: AdvisorQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ask a question to an advisor.
    
    - Sends question to Perplexity API with advisor's system prompt
    - Includes user's birth chart context
    - Stores conversation in database
    - Returns AI-generated response
    
    Note: Perplexity API integration needed
    """
    # Get advisor
    advisor = db.query(Advisor).filter(
        Advisor.id == query.advisor_id,
        Advisor.is_active == True
    ).first()
    
    if not advisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advisor not found"
        )
    
    # Get user's birth chart for context
    chart = db.query(BirthChart).filter(
        BirthChart.user_id == current_user.id
    ).first()
    
    chart_context = {}
    if chart:
        chart_context = {
            "current_mahadasha": chart.current_mahadasha,
            "current_antardasha": chart.current_antardasha,
            "birth_location": chart.birth_location
        }
    
    # TODO: Call Perplexity API
    # This would use the advisor's system_prompt and include chart_context
    # For now, placeholder response
    
    # from openai import OpenAI
    # client = OpenAI(
    #     api_key=settings.PERPLEXITY_API_KEY,
    #     base_url="https://api.perplexity.ai"
    # )
    # 
    # response = client.chat.completions.create(
    #     model="llama-3.1-sonar-large-128k-online",
    #     messages=[
    #         {"role": "system", "content": advisor.system_prompt},
    #         {"role": "user", "content": f"Context: {chart_context}\n\nQuestion: {query.question}"}
    #     ]
    # )
    # 
    # ai_response = response.choices[0].message.content
    
    # Placeholder response
    ai_response = f"This is {advisor.name} speaking. I hear your question: '{query.question}'. (Perplexity API integration coming soon - this is a placeholder response.)"
    
    # Store message in database
    message = Message(
        user_id=current_user.id,
        advisor_id=advisor.id,
        question=query.question,
        response=ai_response,
        chart_context=chart_context
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


@router.get("/history", response_model=list[MessageResponse])
async def get_conversation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    advisor_id: str = None,
    limit: int = 50
):
    """
    Get conversation history with advisors.
    
    - Returns recent messages
    - Optionally filter by advisor_id
    - Sorted by most recent first
    """
    query_obj = db.query(Message).filter(Message.user_id == current_user.id)
    
    if advisor_id:
        query_obj = query_obj.filter(Message.advisor_id == advisor_id)
    
    messages = query_obj.order_by(
        Message.created_at.desc()
    ).limit(limit).all()
    
    return messages
