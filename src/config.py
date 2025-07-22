"""
script that hold the configuration of our application
"""

# ─── Streamlit page settings ──────────────────────────────────────────────────
PAGE_CONFIG = {
    'Page_title' : "Spring Change Detection",
    'layout': "wide", # centred
    'initial_sidebar_state': "auto", #collapsed, expanded
    'Page_icon': "🚗",
    }

# ─── Upload restrictions ──────────────────────────────────────────────────────
UPLOAD_CONFIG = {
    "allowed_extension": ['xlsx', 'xls'],
    "max_file_size" : 200,
    "sheet_name": "PTA",
    "skip_rows": [1]
    }

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