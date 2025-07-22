"""
script that hold the configuration of our application
"""

# ─── Streamlit page settings ──────────────────────────────────────────────────
PAGE_TITLE: str = "Spring Change Detection"
PAGE_ICON: str = "🚗"
PAGE_LAYOUT: str = "wide" #centred
INITIAL_SIDEBAR_STATE: str = "auto" #collapsed, expanded

# ─── Upload restrictions ──────────────────────────────────────────────────────
UPLOAD_ALLOWED_EXTENSIONS = ["xlsx", "xls"]
UPLOAD_MAX_FILE_SIZE_MB: int = 200
UPLOAD_SHEET_NAME: str = "PTA"
UPLOAD_SKIP_ROWS = [1]

# ─── Columns Data ────────────────────────────────────────────────────
REQUIRED_COLUMNS: dict = {
    "mass": "Masse suspendue en charge de référence",
    "reference": "Référence"
}

VP_COLUMNS_KEY: list = [
        "Moteur", "Boite", "Niveau",
        "Plaque de protection tôle sous GMP",
        "Pavillon multifonction", "2e PLC Gauche",
        "Chauffage additionnel type WEBASTO"   
        ]

VU_COLUMNS_KEY: list =[
    "Moteur", "Boite", "Niveau", "Plaque de conception"
]