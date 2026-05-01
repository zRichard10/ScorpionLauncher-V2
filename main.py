"""Scorpion Launcher v2.0 – Premium Minecraft Launcher"""
import customtkinter as ctk
import os, threading, time
from tkinter import messagebox, filedialog
from datetime import datetime
from config import C, ConfigManager, ALL_VERSIONS, ASSETS_DIR, APP_VERSION
from mc_manager import MinecraftManager

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ctk.set_appearance_mode("dark")

# ═══════════════════════════════════════════════════════════
class ScorpionLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scorpion Launcher")
        self.geometry("1050x660")
        self.minsize(900, 580)
        self.configure(fg_color=C.BG_PRIMARY)
        # Set window icon
        ico_path = os.path.join(ASSETS_DIR, "icon.ico")
        png_path = os.path.join(ASSETS_DIR, "icon.png")
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)
            self.after(200, lambda: self.iconbitmap(ico_path))
        self._logo_img = None
        if HAS_PIL and os.path.exists(png_path):
            self._logo_img = ctk.CTkImage(Image.open(png_path), size=(48, 48))
        self.config_mgr = ConfigManager()
        self.mc = MinecraftManager(self.config_mgr)
        self.pages = {}
        self.active_btn = None
        self._build_sidebar()
        self._build_content()
        self._build_pages()
        self.show_page("home")

    # ── Sidebar ─────────────────────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=230, fg_color=C.BG_SIDEBAR, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        # Logo
        logo_f = ctk.CTkFrame(sb, fg_color="transparent", height=100)
        logo_f.pack(fill="x", pady=(25, 5), padx=15)
        logo_f.pack_propagate(False)
        if self._logo_img:
            ctk.CTkLabel(logo_f, image=self._logo_img, text="").pack(anchor="w")
        else:
            ctk.CTkLabel(logo_f, text="🦂", font=ctk.CTkFont(size=36)).pack(anchor="w")
        ctk.CTkLabel(logo_f, text="SCORPION", font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=C.ACCENT).pack(anchor="w")
        ctk.CTkLabel(logo_f, text="LAUNCHER", font=ctk.CTkFont("Segoe UI", 11),
                     text_color=C.TEXT_SEC).pack(anchor="w")
        # Separator
        ctk.CTkFrame(sb, height=1, fg_color=C.BORDER).pack(fill="x", padx=20, pady=12)
        # Nav buttons
        self.nav_btns = {}
        nav = [("home","🏠","Inicio"),("versions","📦","Versiones"),("settings","⚙️","Ajustes")]
        for key, icon, label in nav:
            b = ctk.CTkButton(sb, text=f"  {icon}   {label}", anchor="w", height=44,
                              corner_radius=10, font=ctk.CTkFont("Segoe UI", 14),
                              fg_color="transparent", text_color=C.TEXT_SEC,
                              hover_color=C.BG_SIDEBAR_HOV,
                              command=lambda k=key: self.show_page(k))
            b.pack(fill="x", padx=12, pady=2)
            self.nav_btns[key] = b
        # Bottom version
        ctk.CTkLabel(sb, text=f"v{APP_VERSION}", text_color=C.TEXT_MUTED,
                     font=ctk.CTkFont(size=11)).pack(side="bottom", pady=15)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=C.BG_PRIMARY, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

    def show_page(self, name):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill="both", expand=True, padx=28, pady=20)
        for k, b in self.nav_btns.items():
            if k == name:
                b.configure(fg_color=C.BG_SIDEBAR_ACT, text_color=C.ACCENT)
            else:
                b.configure(fg_color="transparent", text_color=C.TEXT_SEC)

    def _build_pages(self):
        self.pages["home"] = self._page_home()
        self.pages["versions"] = self._page_versions()
        self.pages["settings"] = self._page_settings()

    # ── HOME PAGE ───────────────────────────────────────────
    def _page_home(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        # Banner
        banner = ctk.CTkFrame(page, height=180, fg_color=C.BG_CARD, corner_radius=16)
        banner.pack(fill="x", pady=(0, 20))
        banner.pack_propagate(False)
        banner_path = os.path.join(ASSETS_DIR, "banner.png")
        if HAS_PIL and os.path.exists(banner_path):
            img = ctk.CTkImage(Image.open(banner_path), size=(780, 180))
            ctk.CTkLabel(banner, image=img, text="").pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(banner, text="🦂 SCORPION LAUNCHER",
                         font=ctk.CTkFont("Segoe UI", 32, "bold"),
                         text_color=C.ACCENT).pack(expand=True)
        # Play card
        card = ctk.CTkFrame(page, fg_color=C.BG_CARD, corner_radius=16, border_width=1,
                            border_color=C.BORDER)
        card.pack(fill="x", pady=(0, 20))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=30, pady=25, fill="x")
        ctk.CTkLabel(inner, text="⚡ Jugar Minecraft",
                     font=ctk.CTkFont("Segoe UI", 20, "bold"),
                     text_color=C.TEXT).pack(anchor="w")
        ctk.CTkLabel(inner, text="Selecciona versión y usuario para iniciar",
                     font=ctk.CTkFont(size=13), text_color=C.TEXT_SEC).pack(anchor="w", pady=(2,15))
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")
        # Version selector
        col1 = ctk.CTkFrame(row, fg_color="transparent")
        col1.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkLabel(col1, text="Versión", text_color=C.TEXT_SEC,
                     font=ctk.CTkFont(size=12)).pack(anchor="w")
        installed = self.mc.get_installed()
        ver_list = installed if installed else ["Sin versiones"]
        self.home_version = ctk.StringVar(value=self.config_mgr.get("last_version") or ver_list[0])
        self.home_ver_menu = ctk.CTkOptionMenu(col1, variable=self.home_version, values=ver_list,
                                                fg_color=C.BG_INPUT, button_color=C.ACCENT_DARK,
                                                button_hover_color=C.ACCENT, dropdown_fg_color=C.BG_CARD,
                                                width=220, height=38, corner_radius=10)
        self.home_ver_menu.pack(anchor="w", pady=(4,0))
        # Username
        col2 = ctk.CTkFrame(row, fg_color="transparent")
        col2.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkLabel(col2, text="Usuario", text_color=C.TEXT_SEC,
                     font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.home_user = ctk.CTkEntry(col2, placeholder_text="Tu nombre de usuario",
                                       fg_color=C.BG_INPUT, border_color=C.BORDER,
                                       width=220, height=38, corner_radius=10)
        self.home_user.pack(anchor="w", pady=(4,0))
        saved_user = self.config_mgr.get("username", "")
        if saved_user:
            self.home_user.insert(0, saved_user)
        # Play button
        col3 = ctk.CTkFrame(row, fg_color="transparent")
        col3.pack(side="right", padx=(10,0))
        ctk.CTkLabel(col3, text=" ", font=ctk.CTkFont(size=12)).pack()
        self.play_btn = ctk.CTkButton(col3, text="▶  JUGAR", width=160, height=42,
                                       corner_radius=12, font=ctk.CTkFont("Segoe UI", 15, "bold"),
                                       fg_color=C.ACCENT, hover_color=C.ACCENT_DARK,
                                       text_color="#000000", command=self._play)
        self.play_btn.pack(pady=(4,0))
        # Stats row
        stats = ctk.CTkFrame(page, fg_color="transparent")
        stats.pack(fill="x")
        for title, value, color in [
            ("Instaladas", str(len(installed)), C.ACCENT),
            ("RAM", f"{self.config_mgr.get('ram_gb', 4)} GB", C.BLUE),
            ("Sesiones", str(self.config_mgr.get("play_count", 0)), C.GREEN),
        ]:
            sc = ctk.CTkFrame(stats, fg_color=C.BG_CARD, corner_radius=14, border_width=1,
                              border_color=C.BORDER)
            sc.pack(side="left", fill="x", expand=True, padx=(0,12))
            sp = ctk.CTkFrame(sc, fg_color="transparent")
            sp.pack(padx=20, pady=16)
            ctk.CTkLabel(sp, text=value, font=ctk.CTkFont("Segoe UI", 28, "bold"),
                         text_color=color).pack(anchor="w")
            ctk.CTkLabel(sp, text=title, font=ctk.CTkFont(size=12),
                         text_color=C.TEXT_SEC).pack(anchor="w")
        return page

    # ── VERSIONS PAGE ───────────────────────────────────────
    def _page_versions(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        ctk.CTkLabel(page, text="📦 Gestión de Versiones",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=C.TEXT).pack(anchor="w", pady=(0,5))
        ctk.CTkLabel(page, text="Instala, elimina y administra tus versiones de Minecraft",
                     font=ctk.CTkFont(size=13), text_color=C.TEXT_SEC).pack(anchor="w", pady=(0,18))
        # Install card
        ic = ctk.CTkFrame(page, fg_color=C.BG_CARD, corner_radius=14, border_width=1,
                          border_color=C.BORDER)
        ic.pack(fill="x", pady=(0,18))
        icp = ctk.CTkFrame(ic, fg_color="transparent")
        icp.pack(padx=24, pady=20, fill="x")
        ctk.CTkLabel(icp, text="Instalar nueva versión",
                     font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C.TEXT).pack(anchor="w")
        ir = ctk.CTkFrame(icp, fg_color="transparent")
        ir.pack(fill="x", pady=(10,0))
        available = self.mc.get_available()
        self.install_ver = ctk.StringVar(value=available[0] if available else "—")
        self.install_menu = ctk.CTkOptionMenu(ir, variable=self.install_ver,
                                               values=available if available else ["—"],
                                               fg_color=C.BG_INPUT, button_color=C.ACCENT_DARK,
                                               button_hover_color=C.ACCENT,
                                               dropdown_fg_color=C.BG_CARD,
                                               width=240, height=38, corner_radius=10)
        self.install_menu.pack(side="left", padx=(0,12))
        self.install_btn = ctk.CTkButton(ir, text="⬇  Descargar", width=150, height=38,
                                          corner_radius=10, fg_color=C.ACCENT,
                                          hover_color=C.ACCENT_DARK, text_color="#000",
                                          font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                          command=self._install_version)
        self.install_btn.pack(side="left")
        # Progress
        self.prog_frame = ctk.CTkFrame(icp, fg_color="transparent")
        self.prog_frame.pack(fill="x", pady=(12,0))
        self.prog_label = ctk.CTkLabel(self.prog_frame, text="", text_color=C.TEXT_SEC,
                                        font=ctk.CTkFont(size=12))
        self.prog_label.pack(anchor="w")
        self.prog_bar = ctk.CTkProgressBar(self.prog_frame, fg_color=C.BG_INPUT,
                                            progress_color=C.ACCENT, height=8, corner_radius=4)
        self.prog_bar.pack(fill="x", pady=(4,0))
        self.prog_bar.set(0)
        self.prog_frame.pack_forget()
        # Installed list
        ctk.CTkLabel(page, text="Versiones instaladas",
                     font=ctk.CTkFont("Segoe UI", 16, "bold"),
                     text_color=C.TEXT).pack(anchor="w", pady=(0,10))
        self.ver_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent",
                                                  scrollbar_button_color=C.BORDER)
        self.ver_scroll.pack(fill="both", expand=True)
        self._refresh_installed_list()
        return page

    def _refresh_installed_list(self):
        for w in self.ver_scroll.winfo_children():
            w.destroy()
        installed = self.mc.get_installed()
        if not installed:
            ctk.CTkLabel(self.ver_scroll, text="No hay versiones instaladas aún.",
                         text_color=C.TEXT_MUTED).pack(pady=30)
            return
        for v in installed:
            row = ctk.CTkFrame(self.ver_scroll, fg_color=C.BG_CARD, corner_radius=12,
                               height=50, border_width=1, border_color=C.BORDER)
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)
            ctk.CTkLabel(row, text=f"  🟢  Minecraft {v}",
                         font=ctk.CTkFont("Segoe UI", 13),
                         text_color=C.TEXT).pack(side="left", padx=12)
            ctk.CTkButton(row, text="▶ Jugar", width=80, height=30, corner_radius=8,
                          fg_color=C.ACCENT, hover_color=C.ACCENT_DARK, text_color="#000",
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=lambda ver=v: self._quick_play(ver)).pack(side="right", padx=(0,10), pady=10)

    def _refresh_home_versions(self):
        installed = self.mc.get_installed()
        ver_list = installed if installed else ["Sin versiones"]
        self.home_ver_menu.configure(values=ver_list)
        if installed:
            self.home_version.set(installed[0])

    # ── SETTINGS PAGE ───────────────────────────────────────
    def _page_settings(self):
        page = ctk.CTkScrollableFrame(self.content, fg_color="transparent",
                                       scrollbar_button_color=C.BORDER)
        ctk.CTkLabel(page, text="⚙️  Configuración",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=C.TEXT).pack(anchor="w", pady=(0,18))
        # RAM
        rc = self._settings_card(page, "Memoria RAM",
                                  "Cantidad de RAM asignada a Minecraft")
        rf = ctk.CTkFrame(rc, fg_color="transparent")
        rf.pack(fill="x", pady=(8,0))
        self.ram_val = ctk.IntVar(value=self.config_mgr.get("ram_gb", 4))
        self.ram_label = ctk.CTkLabel(rf, text=f"{self.ram_val.get()} GB",
                                       font=ctk.CTkFont("Segoe UI", 18, "bold"),
                                       text_color=C.ACCENT)
        self.ram_label.pack(anchor="w")
        self.ram_slider = ctk.CTkSlider(rf, from_=1, to=16, number_of_steps=15,
                                         variable=self.ram_val,
                                         fg_color=C.BG_INPUT, progress_color=C.ACCENT,
                                         button_color=C.ACCENT, button_hover_color=C.ACCENT_LIGHT,
                                         command=self._on_ram_change)
        self.ram_slider.pack(fill="x", pady=(6,0))
        lr = ctk.CTkFrame(rf, fg_color="transparent")
        lr.pack(fill="x")
        ctk.CTkLabel(lr, text="1 GB", text_color=C.TEXT_MUTED, font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkLabel(lr, text="16 GB", text_color=C.TEXT_MUTED, font=ctk.CTkFont(size=11)).pack(side="right")
        # Minecraft Dir
        dc = self._settings_card(page, "Directorio de Minecraft",
                                  "Ubicación de la carpeta .minecraft")
        df = ctk.CTkFrame(dc, fg_color="transparent")
        df.pack(fill="x", pady=(8,0))
        self.dir_entry = ctk.CTkEntry(df, fg_color=C.BG_INPUT, border_color=C.BORDER,
                                       height=38, corner_radius=10)
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.dir_entry.insert(0, self.config_mgr.get("minecraft_dir", ""))
        ctk.CTkButton(df, text="📁", width=42, height=38, corner_radius=10,
                      fg_color=C.ACCENT, hover_color=C.ACCENT_DARK, text_color="#000",
                      command=self._browse_dir).pack(side="right")
        # Java Path
        jc = self._settings_card(page, "Ruta de Java (opcional)",
                                  "Dejar vacío para usar Java del sistema")
        jf = ctk.CTkFrame(jc, fg_color="transparent")
        jf.pack(fill="x", pady=(8,0))
        self.java_entry = ctk.CTkEntry(jf, fg_color=C.BG_INPUT, border_color=C.BORDER,
                                        height=38, corner_radius=10,
                                        placeholder_text="Automático")
        self.java_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        jp = self.config_mgr.get("java_path", "")
        if jp:
            self.java_entry.insert(0, jp)
        ctk.CTkButton(jf, text="📁", width=42, height=38, corner_radius=10,
                      fg_color=C.ACCENT, hover_color=C.ACCENT_DARK, text_color="#000",
                      command=self._browse_java).pack(side="right")
        # Users
        uc = self._settings_card(page, "Usuarios guardados",
                                  "Administra tus perfiles de usuario")
        self.users_frame = ctk.CTkFrame(uc, fg_color="transparent")
        self.users_frame.pack(fill="x", pady=(8,0))
        self._refresh_users_list()
        # Save
        ctk.CTkButton(page, text="💾  Guardar Configuración", height=44, corner_radius=12,
                      fg_color=C.ACCENT, hover_color=C.ACCENT_DARK, text_color="#000",
                      font=ctk.CTkFont("Segoe UI", 14, "bold"),
                      command=self._save_settings).pack(fill="x", pady=(20,10))
        return page

    def _settings_card(self, parent, title, subtitle):
        card = ctk.CTkFrame(parent, fg_color=C.BG_CARD, corner_radius=14,
                            border_width=1, border_color=C.BORDER)
        card.pack(fill="x", pady=(0,14))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=24, pady=18, fill="x")
        ctk.CTkLabel(inner, text=title, font=ctk.CTkFont("Segoe UI", 15, "bold"),
                     text_color=C.TEXT).pack(anchor="w")
        ctk.CTkLabel(inner, text=subtitle, font=ctk.CTkFont(size=12),
                     text_color=C.TEXT_SEC).pack(anchor="w", pady=(2,0))
        return inner

    def _refresh_users_list(self):
        for w in self.users_frame.winfo_children():
            w.destroy()
        users = self.config_mgr.get("users", [])
        if not users:
            ctk.CTkLabel(self.users_frame, text="Sin usuarios guardados",
                         text_color=C.TEXT_MUTED).pack(anchor="w")
            return
        for u in users:
            r = ctk.CTkFrame(self.users_frame, fg_color=C.BG_INPUT, corner_radius=8, height=36)
            r.pack(fill="x", pady=2)
            r.pack_propagate(False)
            ctk.CTkLabel(r, text=f"  👤  {u}", text_color=C.TEXT,
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=8)
            ctk.CTkButton(r, text="✕", width=30, height=26, corner_radius=6,
                          fg_color=C.RED, hover_color="#dc2626", text_color="#fff",
                          font=ctk.CTkFont(size=12),
                          command=lambda name=u: self._del_user(name)).pack(side="right", padx=6, pady=5)

    # ── Actions ─────────────────────────────────────────────
    def _play(self):
        version = self.home_version.get()
        username = self.home_user.get().strip()
        if not username:
            messagebox.showerror("Error", "Escribe un nombre de usuario.")
            return
        if version in ("Sin versiones", ""):
            messagebox.showerror("Error", "No hay versiones instaladas.")
            return
        self.config_mgr.add_user(username)
        self.config_mgr.set("username", username)
        self.config_mgr.set("last_version", version)
        self.config_mgr.set("play_count", self.config_mgr.get("play_count", 0) + 1)
        self.config_mgr.set("last_played", datetime.now().isoformat())
        ram = self.config_mgr.get("ram_gb", 4)
        java = self.config_mgr.get("java_path", "")
        self.play_btn.configure(text="⏳ Iniciando...", state="disabled")
        result = self.mc.launch(version, username, ram, java)
        if result is True:
            self.after(3000, lambda: self.play_btn.configure(text="▶  JUGAR", state="normal"))
        else:
            messagebox.showerror("Error", f"No se pudo iniciar:\n{result}")
            self.play_btn.configure(text="▶  JUGAR", state="normal")

    def _quick_play(self, version):
        self.home_version.set(version)
        self.show_page("home")

    def _install_version(self):
        version = self.install_ver.get()
        if version == "—":
            return
        self.prog_frame.pack(fill="x", pady=(12,0))
        self.prog_bar.set(0)
        self.prog_label.configure(text=f"Preparando descarga de {version}...")
        self.install_btn.configure(state="disabled", text="⏳ Descargando...")
        self._max_prog = 0

        def on_status(s):
            self.after(0, lambda: self.prog_label.configure(text=s))
        def on_max(m):
            self._max_prog = m
        def on_progress(p):
            if self._max_prog > 0:
                self.after(0, lambda: self.prog_bar.set(p / self._max_prog))

        def do_install():
            cb = {"setStatus": on_status, "setMax": on_max, "setProgress": on_progress}
            result = self.mc.install(version, callback=cb)
            self.after(0, lambda: self._on_install_done(version, result))

        threading.Thread(target=do_install, daemon=True).start()

    def _on_install_done(self, version, result):
        self.install_btn.configure(state="normal", text="⬇  Descargar")
        if result is True:
            self.prog_label.configure(text=f"✅ Minecraft {version} instalado correctamente")
            self.prog_bar.set(1)
            self._refresh_installed_list()
            self._refresh_home_versions()
            available = self.mc.get_available()
            self.install_menu.configure(values=available if available else ["—"])
            if available:
                self.install_ver.set(available[0])
            else:
                self.install_ver.set("—")
        else:
            self.prog_label.configure(text=f"❌ Error: {result}")
            messagebox.showerror("Error", f"No se pudo instalar:\n{result}")

    def _on_ram_change(self, val):
        v = int(val)
        self.ram_label.configure(text=f"{v} GB")

    def _browse_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, d)

    def _browse_java(self):
        f = filedialog.askopenfilename(filetypes=[("Java", "javaw.exe;java.exe")])
        if f:
            self.java_entry.delete(0, "end")
            self.java_entry.insert(0, f)

    def _save_settings(self):
        self.config_mgr.set("ram_gb", int(self.ram_slider.get()))
        self.config_mgr.set("minecraft_dir", self.dir_entry.get())
        self.config_mgr.set("java_path", self.java_entry.get())
        self.mc.mc_dir = self.dir_entry.get()
        messagebox.showinfo("Guardado", "Configuración guardada correctamente.")

    def _del_user(self, name):
        self.config_mgr.remove_user(name)
        self._refresh_users_list()

if __name__ == "__main__":
    app = ScorpionLauncher()
    app.mainloop()
