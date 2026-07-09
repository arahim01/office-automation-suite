from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.manager.models import Module

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/api/modules")
def list_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).order_by(Module.id).all()
    return [
        {
            "slug": m.slug,
            "name": m.name,
            "priority": m.priority,
            "status": m.status,
            "last_run": m.last_run,
            "notes": m.notes,
        }
        for m in modules
    ]


@router.patch("/api/modules/{slug}/status")
def update_status(slug: str, status: str, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.slug == slug).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    module.status = status
    module.last_run = datetime.now(timezone.utc)
    db.commit()
    return {"slug": slug, "status": module.status}


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    modules = db.query(Module).order_by(Module.id).all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "modules": modules}
    )
