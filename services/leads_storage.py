import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
LEADS_FILE = DATA_DIR / "leads.json"

def _ensure_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not LEADS_FILE.exists():
        LEADS_FILE.write_text("[]", encoding="utf-8")

def save_lead(lead: dict):
    _ensure_file()
    leads = get_all_leads()
    lead["created_at"] = datetime.now().isoformat()
    leads.append(lead)
    LEADS_FILE.write_text(json.dumps(leads, ensure_ascii=False, indent=2), encoding="utf-8")

def get_all_leads() -> list:
    _ensure_file()
    try:
        return json.loads(LEADS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
