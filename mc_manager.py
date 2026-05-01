"""
Scorpion Launcher v2.0 - Minecraft Manager
Handles version installation, listing, and game launching.
"""
import subprocess
import uuid
import minecraft_launcher_lib

from config import ALL_VERSIONS, APP_VERSION, ConfigManager


class MinecraftManager:
    """High-level wrapper around minecraft_launcher_lib."""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.mc_dir: str = config.get("minecraft_dir")

    # ── Versions ────────────────────────────────────────────
    def get_installed(self) -> list[str]:
        try:
            versions = minecraft_launcher_lib.utils.get_installed_versions(self.mc_dir)
            return [v["id"] for v in versions]
        except Exception:
            return []

    def get_available(self) -> list[str]:
        installed = set(self.get_installed())
        return [v for v in ALL_VERSIONS if v not in installed]

    # ── Install ─────────────────────────────────────────────
    def install(self, version: str, callback=None) -> bool | str:
        """Install *version*. Returns True on success, error string on failure."""
        try:
            minecraft_launcher_lib.install.install_minecraft_version(
                version, self.mc_dir, callback=callback
            )
            return True
        except Exception as e:
            return str(e)

    # ── Launch ──────────────────────────────────────────────
    def launch(self, version: str, username: str,
               ram_gb: int = 4, java_path: str = "") -> bool | str:
        """Launch Minecraft. Returns True on success, error string on failure."""
        options = {
            "username": username,
            "uuid": str(uuid.uuid4()),
            "token": "",
            "jvmArguments": [
                f"-Xmx{ram_gb}G",
                f"-Xms{max(1, ram_gb // 2)}G",
            ],
            "launcherVersion": APP_VERSION,
        }
        if java_path and __import__("os").path.exists(java_path):
            options["executablePath"] = java_path

        try:
            command = minecraft_launcher_lib.command.get_minecraft_command(
                version, self.mc_dir, options
            )
            subprocess.Popen(command)
            return True
        except Exception as e:
            return str(e)
