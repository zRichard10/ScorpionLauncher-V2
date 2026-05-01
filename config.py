"""
Scorpion Launcher v2.0 - Configuration Module
Handles persistent settings, color theme, and constants.
"""
import os
import json

APP_NAME = "Scorpion Launcher"
APP_VERSION = "2.0.0"

# ── Paths ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CONFIG_FILE = os.path.join(BASE_DIR, "launcher_config.json")
DEFAULT_MC_DIR = os.path.join(
    os.path.expanduser("~"), "AppData", "Roaming", ".minecraft"
)

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DEFAULT_MC_DIR, exist_ok=True)

# ── Color Palette ──────────────────────────────────────────
class C:
    """Scorpion Dark Theme – Amber Accents."""
    BG_DARKEST      = "#080808"
    BG_DARK         = "#0c0c0c"
    BG_PRIMARY      = "#111111"
    BG_SECONDARY    = "#181818"
    BG_CARD         = "#1c1c1c"
    BG_CARD_HOVER   = "#262626"
    BG_INPUT        = "#1e1e1e"
    BG_SIDEBAR      = "#0a0a0a"
    BG_SIDEBAR_ACT  = "#1a1610"
    BG_SIDEBAR_HOV  = "#141414"
    ACCENT          = "#f59e0b"
    ACCENT_DARK     = "#d97706"
    ACCENT_LIGHT    = "#fbbf24"
    GREEN           = "#22c55e"
    RED             = "#ef4444"
    BLUE            = "#3b82f6"
    TEXT            = "#f5f5f5"
    TEXT_SEC         = "#9ca3af"
    TEXT_MUTED      = "#555555"
    BORDER          = "#2a2a2a"
    BORDER_SUBTLE   = "#222222"

# ── Supported Minecraft Versions ───────────────────────────
_FALLBACK_VERSIONS = [
    "1.21.5", "1.21.4", "1.21.3", "1.21.1", "1.21",
    "1.20.6", "1.20.4", "1.20.2", "1.20.1", "1.20",
    "1.19.4", "1.19.3", "1.19.2", "1.19",
    "1.18.2", "1.18.1", "1.18",
    "1.17.1", "1.17",
    "1.16.5", "1.16.4", "1.16.1",
    "1.15.2", "1.14.4", "1.13.2",
    "1.12.2", "1.12",
    "1.11.2", "1.10.2", "1.9.4",
    "1.8.9", "1.8",
    "1.7.10",
]

def fetch_all_versions():
    """Fetch release versions from Mojang API. Falls back to hardcoded list offline."""
    try:
        import minecraft_launcher_lib
        raw = minecraft_launcher_lib.utils.get_version_list()
        # Only keep "release" type, sorted newest first
        releases = [v["id"] for v in raw if v.get("type") == "release"]
        return releases if releases else _FALLBACK_VERSIONS
    except Exception:
        return _FALLBACK_VERSIONS

ALL_VERSIONS = fetch_all_versions()

# ── Persistent Config Manager ──────────────────────────────
class ConfigManager:
    def __init__(self):
        self.data = self._load()

    # ── private ─────────────────────────────────────────────
    def _load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._defaults()

    @staticmethod
    def _defaults():
        return {
            "username": "",
            "last_version": "",
            "ram_gb": 4,
            "minecraft_dir": DEFAULT_MC_DIR,
            "java_path": "",
            "users": [],
            "fullscreen": False,
            "last_played": None,
            "play_count": 0,
        }

    # ── public ──────────────────────────────────────────────
    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def add_user(self, username: str):
        users = self.data.get("users", [])
        if username and username not in users:
            users.insert(0, username)
            self.data["users"] = users[:10]
            self.save()

    def remove_user(self, username: str):
        users = self.data.get("users", [])
        if username in users:
            users.remove(username)
            self.data["users"] = users
            self.save()
