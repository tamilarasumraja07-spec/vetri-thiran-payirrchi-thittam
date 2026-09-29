from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "PocketSmart AI",
        },
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Login",
        },
    )


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Register",
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Dashboard",
        },
    )


@router.get(
    "/planner/home",
    response_class=HTMLResponse,
)
def home_planner(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Home Interior Planner",
        },
    )


@router.get(
    "/planner/party",
    response_class=HTMLResponse,
)
def party_planner(request: Request):
    return templates.TemplateResponse(
        "party.html",
        {
            "request": request,
            "title": "Party Planner",
        },
    )


@router.get(
    "/planner/jewelry",
    response_class=HTMLResponse,
)
def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        "jewelry.html",
        {
            "request": request,
            "title": "Jewelry Planner",
        },
    )


@router.get(
    "/testimonials",
    response_class=HTMLResponse,
)
def testimonials_page(request: Request):
    return templates.TemplateResponse(
        "testimonials.html",
        {
            "request": request,
            "title": "Testimonials",
        },
    )