"""Create desktop shortcut for Scorpion Launcher (run once)."""
import os, sys

try:
    import winshell
    HAS_WINSHELL = True
except ImportError:
    HAS_WINSHELL = False

def create_shortcut():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    base = os.path.dirname(os.path.abspath(__file__))
    vbs = os.path.join(base, "ScorpionLauncher.vbs")
    ico = os.path.join(base, "assets", "icon.ico")
    lnk = os.path.join(desktop, "Scorpion Launcher.lnk")

    # Method 1: Using win32com (most reliable)
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk)
        shortcut.TargetPath = vbs
        shortcut.WorkingDirectory = base
        shortcut.IconLocation = f"{ico},0"
        shortcut.Description = "Scorpion Launcher - Minecraft"
        shortcut.save()
        print(f"[OK] Acceso directo creado en: {lnk}")
        return True
    except ImportError:
        pass

    # Method 2: PowerShell script file
    ps_script = os.path.join(base, "_make_shortcut.ps1")
    with open(ps_script, "w", encoding="utf-8") as f:
        f.write(f'''$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut("{lnk}")
$s.TargetPath = "{vbs}"
$s.WorkingDirectory = "{base}"
$s.IconLocation = "{ico},0"
$s.Description = "Scorpion Launcher - Minecraft"
$s.Save()
Write-Host "Shortcut created"
''')
    os.system(f'powershell -ExecutionPolicy Bypass -File "{ps_script}"')
    os.remove(ps_script)

    if os.path.exists(lnk):
        print(f"[OK] Acceso directo creado en: {lnk}")
        return True
    else:
        print("[ERROR] No se pudo crear el acceso directo automaticamente.")
        print(f"   Crea uno manualmente apuntando a: {vbs}")
        print(f"   Con ícono: {ico}")
        return False

if __name__ == "__main__":
    create_shortcut()
