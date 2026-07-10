from fastapi import FastAPI

from app.core.database import Base, SessionLocal, engine
from app.manager import routes as manager_routes
from app.manager.models import Module

app = FastAPI(title="Office Automation Suite")

app.include_router(manager_routes.router)

SEED_MODULES = [
    ("invoice_parser", "Invoice Parser", "Existing"),
    ("meeting_summary", "Meeting Summary (Daily Digest)", "Existing"),
    ("appt_scheduling", "Appointment Scheduling", "High"),
    ("appt_prep", "Appointment Prep Research", "High"),
    ("email_mgmt", "Email Management", "High"),
    ("lead_gen", "Lead Generation", "Medium"),
    ("prospecting", "Prospecting", "Medium"),
    ("follow_up", "Follow-up", "Medium"),
    ("support", "Customer Support", "Medium"),
    ("content", "Content Creation", "Low"),
]


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = {m.slug for m in db.query(Module).all()}
        for slug, name, priority in SEED_MODULES:
            if slug not in existing:
                db.add(Module(slug=slug, name=name, priority=priority))
        db.commit()
    finally:
        db.close()
