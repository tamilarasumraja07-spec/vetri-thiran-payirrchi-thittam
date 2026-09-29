import json
from typing import Any, Dict, Optional

from app.config import settings


def _currency(value: float) -> str:
    return f"₹{value:,.0f}"


def fallback_home(data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(data["budget"])

    furniture_budget = budget * 0.35
    lighting_budget = budget * 0.15
    electrical_budget = budget * 0.15
    decor_budget = budget * 0.20
    reserve_budget = budget * 0.15

    return {
        "title": "Smart Home Interior Plan",
        "summary": (
            f"A practical {data['style']} plan for "
            f"{data['room_type']} within {_currency(budget)}."
        ),
        "budget": {
            "total": budget,
            "allocation": [
                {
                    "category": "Furniture",
                    "amount": round(furniture_budget),
                },
                {
                    "category": "Lighting",
                    "amount": round(lighting_budget),
                },
                {
                    "category": "Electrical",
                    "amount": round(electrical_budget),
                },
                {
                    "category": "Decor",
                    "amount": round(decor_budget),
                },
                {
                    "category": "Reserve",
                    "amount": round(reserve_budget),
                },
            ],
        },
        "shopping_list": [
            {
                "item": "LED ceiling lights",
                "quantity": data["lights"],
                "reason": "Energy-efficient and suitable for modern interiors.",
            },
            {
                "item": "Ceiling fans",
                "quantity": data["fans"],
                "reason": "Useful for airflow and daily comfort.",
            },
            {
                "item": "Dining table",
                "quantity": data["dining_tables"],
                "reason": "Choose a size appropriate for available floor space.",
            },
        ],
        "tips": [
            "Measure the room before purchasing large furniture.",
            "Keep a portion of the budget for installation.",
            "Compare multiple products before buying.",
            "Prefer products with warranty and return options.",
        ],
    }


def fallback_party(data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(data["budget"])

    catering = budget * 0.45
    decoration = budget * 0.15
    entertainment = budget * 0.15
    venue = budget * 0.15
    reserve = budget * 0.10

    per_guest = budget / max(int(data["guests"]), 1)

    return {
        "title": "Smart Party Budget Plan",
        "summary": (
            f"Plan for {data['guests']} guests for a "
            f"{data['event_type']} event."
        ),
        "budget": {
            "total": budget,
            "per_guest": round(per_guest, 2),
            "allocation": [
                {
                    "category": "Catering",
                    "amount": round(catering),
                },
                {
                    "category": "Decoration",
                    "amount": round(decoration),
                },
                {
                    "category": "Entertainment",
                    "amount": round(entertainment),
                },
                {
                    "category": "Venue",
                    "amount": round(venue),
                },
                {
                    "category": "Reserve",
                    "amount": round(reserve),
                },
            ],
        },
        "recommendations": [
            "Confirm the guest count before finalizing catering.",
            "Keep a small emergency budget.",
            "Compare venue packages rather than only venue rent.",
            "Book important services early.",
        ],
    }


def fallback_jewelry(data: Dict[str, Any]) -> Dict[str, Any]:
    budget = float(data["budget"])

    main_budget = budget * 0.70
    accessory_budget = budget * 0.20
    reserve = budget * 0.10

    return {
        "title": "Smart Jewelry Recommendation",
        "summary": (
            f"Jewelry suggestions for a {data['occasion']} "
            f"with a {data['style']} style."
        ),
        "budget": {
            "total": budget,
            "main_piece": round(main_budget),
            "accessories": round(accessory_budget),
            "reserve": round(reserve),
        },
        "recommendations": [
            {
                "type": "Necklace",
                "style": data["style"],
                "metal": data["metal"],
                "reason": "Choose a design that matches the occasion and outfit neckline.",
            },
            {
                "type": "Earrings",
                "style": data["style"],
                "metal": data["metal"],
                "reason": "Select a complementary rather than overpowering design.",
            },
            {
                "type": "Bracelet",
                "style": data["style"],
                "metal": data["metal"],
                "reason": "A simple bracelet can balance the overall look.",
            },
        ],
        "tips": [
            "Check product certification where applicable.",
            "Compare making charges and return policies.",
            "Choose a comfortable weight for longer events.",
        ],
    }


def _build_prompt(
    category: str,
    data: Dict[str, Any],
) -> str:

    common = """
You are PocketSmart AI, a practical personal shopping and budget
recommendation assistant.

Rules:
1. Respect the user's stated budget.
2. Do not invent live prices, stock availability, ratings, or product links.
3. Give approximate budget allocations rather than claiming exact current prices.
4. Explain why recommendations are suitable.
5. Prioritize value, practicality and the user's requirements.
6. Return valid JSON only.
"""

    if category == "home":
        task = f"""
Create a home interior recommendation.

User data:
{json.dumps(data, indent=2)}

Return JSON with:
title
summary
budget
shopping_list
tips
"""

    elif category == "party":
        task = f"""
Create a party/event budget recommendation.

User data:
{json.dumps(data, indent=2)}

Return JSON with:
title
summary
budget
recommendations
tips
"""

    else:
        task = f"""
Create a jewelry recommendation.

User data:
{json.dumps(data, indent=2)}

Return JSON with:
title
summary
budget
recommendations
tips
"""

    return common + task


def _extract_text(response) -> str:
    text = getattr(response, "text", None)

    if text:
        return text.strip()

    return ""


def _clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def _gemini_generate(
    prompt: str,
    image_bytes: Optional[bytes] = None,
    image_mime: Optional[str] = None,
):
    if not settings.GEMINI_API_KEY:
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        contents = [prompt]

        if image_bytes and image_mime:
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image_mime,
                )
            )

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )

        return _extract_text(response)

    except Exception:
        return None


def generate_recommendation(
    category: str,
    data: Dict[str, Any],
    image_bytes: Optional[bytes] = None,
    image_mime: Optional[str] = None,
):
    prompt = _build_prompt(
        category,
        data,
    )

    ai_text = _gemini_generate(
        prompt,
        image_bytes=image_bytes,
        image_mime=image_mime,
    )

    if ai_text:
        try:
            result = json.loads(
                _clean_json(ai_text)
            )

            return {
                "source": "gemini",
                "data": result,
            }

        except json.JSONDecodeError:
            pass

    if category == "home":
        result = fallback_home(data)

    elif category == "party":
        result = fallback_party(data)

    elif category == "jewelry":
        result = fallback_jewelry(data)

    else:
        result = {
            "title": "Recommendation",
            "summary": "No recommendation available.",
        }

    return {
        "source": "fallback",
        "data": result,
    }