import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entities import RecommendationHistory
from app.models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest,
)
from app.routes.session import current_user
from app.services.recommender import (
    generate_recommendation,
)


router = APIRouter(
    prefix="/api",
    tags=["AI Planners"],
)


def save_history(
    request: Request,
    db: Session,
    category: str,
    input_data: dict,
    result: dict,
):
    user = current_user(
        request,
        db,
    )

    if not user:
        return None

    row = RecommendationHistory(
        user_id=user.id,
        category=category,
        input_json=json.dumps(
            input_data
        ),
        result_json=json.dumps(
            result
        ),
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return row


@router.post("/generate-home")
def generate_home(
    payload: HomeRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    input_data = payload.model_dump()

    result = generate_recommendation(
        "home",
        input_data,
    )

    save_history(
        request,
        db,
        "home",
        input_data,
        result["data"],
    )

    return {
        "success": True,
        "category": "home",
        "source": result["source"],
        "data": result["data"],
    }


@router.post("/generate-party")
def generate_party(
    payload: PartyRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    input_data = payload.model_dump()

    result = generate_recommendation(
        "party",
        input_data,
    )

    save_history(
        request,
        db,
        "party",
        input_data,
        result["data"],
    )

    return {
        "success": True,
        "category": "party",
        "source": result["source"],
        "data": result["data"],
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    metal: str = Form("Any"),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    input_data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "metal": metal,
        "notes": notes,
    }

    image_bytes = None
    image_mime = None

    if outfit_image:
        image_bytes = await outfit_image.read()
        image_mime = outfit_image.content_type

    result = generate_recommendation(
        "jewelry",
        input_data,
        image_bytes=image_bytes,
        image_mime=image_mime,
    )

    save_history(
        request,
        db,
        "jewelry",
        input_data,
        result["data"],
    )

    return {
        "success": True,
        "category": "jewelry",
        "source": result["source"],
        "data": result["data"],
    }