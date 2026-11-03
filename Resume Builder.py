# Created by : @oAmricao
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os
import pathlib
import tempfile
import html
import traceback
import re
import base64
import io

try:
    from PIL import Image, ImageOps
    HAS_PIL = True
except Exception:
    HAS_PIL = False
    Image = None

try:
    from PIL import ImageTk
    HAS_IMAGETK = True
except Exception:
    HAS_IMAGETK = False

BG = "#0f1420"
CARD = "#1a2233"
ACCENT = "#ff8c32"
ACCENT_DARK = "#e2571b"
TEXT = "#e8ecf4"
MUTED = "#8a94a8"
FIELD_BG = "#0f1420"
BORDER = "#2a3450"

THEMES = {
    "نارنجی انرژی": {"accent": "#ff8c32", "dark": "#e2571b", "hero_bg": "linear-gradient(135deg,#ff8c32,#e2571b)", "hero_text": "#ffffff", "h2": "#e2571b", "tag_bg": "#fff3e8", "tag_fg": "#e2571b", "tag_border": "#ffcf9e", "desc": "تم اصلی، گرم و پرانرژی"},
    "طلایی سلطنتی": {"accent": "#d4af37", "dark": "#6b4a00", "hero_bg": "linear-gradient(135deg,#0a0a0a 0%,#2b2300 45%,#d4af37 100%)", "hero_text": "#ffe9a8", "h2": "#8a6d00", "tag_bg": "#fffbe6", "tag_fg": "#6b4a00", "tag_border": "#d4af37", "desc": "مشکی و طلایی لوکس"},
    "نئون سایبری": {"accent": "#00f0ff", "dark": "#7b2ff7", "hero_bg": "linear-gradient(135deg,#05051a,#0a0f3d 55%,#2b0a4d)", "hero_text": "#ccfbff", "h2": "#5b2ee5", "tag_bg": "#0a0f2a", "tag_fg": "#00f0ff", "tag_border": "#00f0ff", "desc": "تیره و نئونی"},
    "کهکشان بنفش": {"accent": "#a78bfa", "dark": "#6d28d9", "hero_bg": "radial-gradient(circle at 80% 20%,#c084fc 0%,#7c3aed 40%,#1e1b4b 100%)", "hero_text": "#ffffff", "h2": "#6d28d9", "tag_bg": "#f5f0ff", "tag_fg": "#6d28d9", "tag_border": "#c4b5fd", "desc": "بنفش خلاق و هنری"},
    "زمرد مدرن": {"accent": "#10b981", "dark": "#065f46", "hero_bg": "linear-gradient(135deg,#022c22,#065f46 55%,#10b981)", "hero_text": "#ffffff", "h2": "#047857", "tag_bg": "#ecfdf5", "tag_fg": "#065f46", "tag_border": "#6ee7b7", "desc": "سبز شیک و مدرن"},
    "ساکورا پاستیلی": {"accent": "#f9a8d4", "dark": "#db2777", "hero_bg": "linear-gradient(135deg,#fdf2f8,#f9a8d4 55%,#ec4899)", "hero_text": "#831843", "h2": "#db2777", "tag_bg": "#fdf2f8", "tag_fg": "#9d174d", "tag_border": "#f9a8d4", "desc": "صورتی لطیف"},
    "فیروزه ایرانی": {"accent": "#14b8a6", "dark": "#0f766e", "hero_bg": "linear-gradient(135deg,#042f2e,#0f766e 60%,#14b8a6)", "hero_text": "#ffffff", "h2": "#0f766e", "tag_bg": "#f0fdfa", "tag_fg": "#0f766e", "tag_border": "#5eead4", "desc": "الهام از کاشی ایرانی"},
    "اقیانوس آبی": {"accent": "#38bdf8", "dark": "#0c4a6e", "hero_bg": "linear-gradient(135deg,#082f49,#0369a1 55%,#38bdf8)", "hero_text": "#ffffff", "h2": "#0369a1", "tag_bg": "#f0f9ff", "tag_fg": "#0c4a6e", "tag_border": "#7dd3fc", "desc": "آبی حرفه‌ای"},
    "مینیمال نوردیک": {"accent": "#334155", "dark": "#0f172a", "hero_bg": "linear-gradient(135deg,#f8fafc,#e2e8f0)", "hero_text": "#0f172a", "h2": "#334155", "tag_bg": "#f8fafc", "tag_fg": "#0f172a", "tag_border": "#94a3b5", "desc": "سفید و خاکستری تمیز"},
    "قرمز اسپرت": {"accent": "#ef4444", "dark": "#7f1d1d", "hero_bg": "linear-gradient(135deg,#050505,#7f1d1d 60%,#ef4444)", "hero_text": "#ffffff", "h2": "#b91c1c", "tag_bg": "#fef2f2", "tag_fg": "#7f1d1d", "tag_border": "#fca5a5", "desc": "مشکی و قرمز جسورانه"},
}

LABELS = {
    "fa": {"about": "درباره من", "skills": "مهارت‌ها", "exp": "سوابق کاری", "edu": "تحصیلات", "certs": "گواهی‌ها و مدارک", "links": "لینک‌ها", "footer": "", "lang": "fa"},
    "en": {"about": "About Me", "skills": "Skills", "exp": "Experience", "edu": "Education", "certs": "Certifications", "links": "Links", "footer": "", "lang": "en"},
}

TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__" dir="__PAGE_DIR__"><head><meta charset="UTF-8">
<title>Resume - __NAME__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
@page { size: A4; margin: 0; }
html,body { height:auto; }
body { font-family:Tahoma,'Segoe UI',sans-serif; background:radial-gradient(1200px 600px at 50% -10%,#243154 0%,#0f1420 60%,#070b14 100%); display:flex; justify-content:center; padding:20px 10px; }
.page { width:210mm; min-height:auto; height:auto; background:linear-gradient(180deg,#ffffff 0%,#f7f8fc 100%); border-radius:22px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,.55),0 8px 24px rgba(0,0,0,.4),0 0 0 1px rgba(255,255,255,.12); display:flex; flex-direction:column; }
@media print { body{ background:#fff; padding:0; display:block; } .page{ box-shadow:none; border-radius:0; width:100%; min-height:297mm; } .card{ box-shadow:none !important; break-inside:avoid; } }
.hero { background:__HERO_BG__; color:__HERO_TEXT__; padding:18px 26px 16px 26px; position:relative; overflow:hidden; box-shadow:inset 0 -12px 30px rgba(0,0,0,.22); }
.hero::before { content:""; position:absolute; width:280px; height:280px; right:-90px; top:-140px; background:rgba(255,255,255,.16); border-radius:50%; }
.hero::after { content:""; position:absolute; width:200px; height:200px; left:-60px; bottom:-110px; background:rgba(255,255,255,.12); border-radius:50%; }
.hero-inner { position:relative; z-index:2; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
.avatar { width:74px; height:74px; min-width:74px; border-radius:50%; background:rgba(255,255,255,.22); border:3px solid rgba(255,255,255,.85); display:flex; align-items:center; justify-content:center; font-size:32px; font-weight:bold; box-shadow:0 10px 24px rgba(0,0,0,.35),0 0 0 5px rgba(255,255,255,.18); flex-shrink:0; }
.avatar-img { width:74px; height:74px; min-width:74px; border-radius:50%; object-fit:cover; object-position:center; border:3px solid rgba(255,255,255,.9); box-shadow:0 10px 24px rgba(0,0,0,.4),0 0 0 5px rgba(255,255,255,.18); flex-shrink:0; display:block; }
.hero h1{ font-size:23px; margin-bottom:3px; letter-spacing:.4px; text-shadow:0 2px 12px rgba(0,0,0,.25); }
.hero-sub{ font-size:12px; opacity:.96; margin:1px 0; }
.content{ flex:0 0 auto; display:flex; flex-direction:column; padding:8px 0 4px 0; height:auto; }
.card{ margin:6px 20px; padding:10px 16px 10px 16px; background:#fff; border-radius:14px; border:1px solid #edf0f7; box-shadow:0 8px 22px rgba(15,20,32,.08),0 2px 5px rgba(15,20,32,.05); height:auto; }
.h2-wrap{ margin-bottom:5px; }
h2{ display:inline-block; font-size:12px; color:__H2__; background:__TAG_BG__; border:1px solid __TAG_BORDER__; border-radius:999px; padding:3px 14px; box-shadow:0 3px 10px rgba(0,0,0,.07),inset 0 1px 0 rgba(255,255,255,.8); }
.card p,.card div.body{ font-size:11.5px; line-height:1.65; color:#2e3442; }
.exp-item{ background:#f8fafc; border:1px solid #eef1f6; border-radius:10px; padding:6px 11px; margin:5px 0; box-shadow:0 3px 10px rgba(0,0,0,.04); }
.exp-title{ font-weight:bold; font-size:11.5px; color:#111827; margin-bottom:1px; }
.tag{ display:inline-block; background:__TAG_BG__; color:__TAG_FG__; border:1px solid __TAG_BORDER__; border-radius:999px; padding:3px 12px; margin:2px; font-size:11.5px; font-weight:normal; font-family:inherit; line-height:1.65; box-shadow:0 3px 10px rgba(0,0,0,.08),inset 0 1px 0 rgba(255,255,255,.7); }
.tag-plain{ font-size:11.5px; font-weight:normal; font-family:inherit; color:#2e3442; }
.tag-sep{ color:__H2__; font-weight:bold; margin:0 8px; }
.link-a{ color:#0369a1; text-decoration:none; word-break:break-all; } .link-a:hover{text-decoration:underline;}
footer{ text-align:center; color:#9aa3b5; padding:6px; font-size:9.5px; }
</style></head><body><div class="page">
<div class="hero"><div class="hero-inner">__HERO_INNER__</div></div>
<div class="content">__SECTIONS__</div>
<footer>__FOOTER__</footer>
</div></body></html>"""

FA_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

def is_fa(s):
    try:
        return bool(FA_RE.search(s or ""))
    except Exception:
        return True

def head_align(title_text, page_dir, align_mode):
    try:
        if align_mode == "center":
            return "center"
        if align_mode in ("right", "left"):
            return align_mode
        if align_mode == "justify":
            return "right" if page_dir == "rtl" else "left"
        if title_text and title_text.strip():
            return "right" if is_fa(title_text) else "left"
        return "right" if page_dir == "rtl" else "left"
    except Exception:
        return "right"

def render_paragraphs(text, page_dir, align_mode):
    try:
        if text is None or not str(text).strip():
            return ""
        lines = str(text).strip().split("\n")
        out = []
        for line in lines:
            if not line.strip():
                continue
            if line.strip() in ("-", "—", "–", "--", "_", "..."):
                continue
            if align_mode == "auto":
                rtl = is_fa(line)
                d = "rtl" if rtl else "ltr"
                a = "right" if rtl else "left"
            else:
                d = page_dir
                a = align_mode
            out.append('<div class="body" dir="' + d + '" style="text-align:' + a + ';">' + html.escape(line.strip()) + '</div>')
        return "".join(out) if out else ""
    except Exception:
        return ""

def image_file_to_datauri(path, max_dim=900, quality=82):
    ext = os.path.splitext(path)[1].lower()
    if HAS_PIL:
        try:
            im = Image.open(path)
            try:
                im = ImageOps.exif_transpose(im)
            except Exception:
                pass
            if im.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                tmp = im.convert("RGBA") if im.mode == "P" else im
                if tmp.mode in ("RGBA", "LA"):
                    bg.paste(tmp, mask=tmp.split()[-1])
                    im = bg
                else:
                    im = im.convert("RGB")
            elif im.mode != "RGB":
                im = im.convert("RGB")
            w, h = im.size
            m = max(w, h)
            if m > max_dim:
                sc = max_dim / float(m)
                im = im.resize((int(w * sc), int(h * sc)), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=quality, optimize=True)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            return "data:image/jpeg;base64," + b64, buf.tell()
        except Exception:
            traceback.print_exc()
    with open(path, "rb") as f:
        data = f.read()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}.get(ext, "image/jpeg")
    return "data:" + mime + ";base64," + base64.b64encode(data).decode("ascii"), len(data)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("رزومه‌ساز - کم/زیاد کردن")
        try:
            sh = self.winfo_screenheight()
            h = min(1000, sh - 70)
            if h < 650:
                h = max(600, sh - 50)
            self.geometry(f"760x{h}")
        except Exception:
            self.geometry("760x950")
        self.minsize(600, 600)
        self.configure(bg=BG)
        self.inputs = {}
        self.skill_items = []
        self.exp_items = []
        self.edu_items = []
        self.cert_items = []
        self.link_items = []
        self.custom_sections = []
        self.theme_name = tk.StringVar(value="زمرد مدرن")
        self.theme_btns = {}
        self.photo_path = None
        self.photo_data_uri = None
        self.photo_thumb_img = None
        self.page_dir = tk.StringVar(value="rtl")
        self.align_mode = tk.StringVar(value="auto")
        self.photo_side = tk.StringVar(value="right")
        self.lang_var = tk.StringVar(value="fa")
        self.skill_layout = tk.StringVar(value="row")
        self.skill_style = tk.StringVar(value="capsule")
        self.show_about = tk.BooleanVar(value=True)
        self.show_skills = tk.BooleanVar(value=True)
        self.show_exp = tk.BooleanVar(value=True)
        self.show_edu = tk.BooleanVar(value=True)
        self.show_certs = tk.BooleanVar(value=True)
        self.show_links = tk.BooleanVar(value=True)
        self.show_title = tk.BooleanVar(value=True)
        self.show_email = tk.BooleanVar(value=True)
        self.show_phone = tk.BooleanVar(value=True)

        tk.Label(self, text="رزومه‌ساز", font=("Tahoma", 18, "bold"), bg=BG, fg=ACCENT).pack(pady=(10, 0))
        tk.Label(self, text="", font=("Tahoma", 10), bg=BG, fg=MUTED).pack(pady=(0, 2))

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(side="bottom", fill="x", padx=22, pady=(4, 6))
        btns = tk.Frame(bottom, bg=BG)
        btns.pack(fill="x", pady=(2, 4))
        tk.Button(btns, text="پیش‌نمایش رزومه", command=self.preview, relief="flat", cursor="hand2", bg=ACCENT, fg="#1a1005", activebackground=ACCENT_DARK, activeforeground="#1a1005", font=("Tahoma", 13, "bold"), pady=12).pack(side="right", fill="x", expand=True, padx=4)
        btns2 = tk.Frame(bottom, bg=BG)
        btns2.pack(fill="x", pady=(0, 4))
        tk.Button(btns2, text="ذخیره با نام", command=self.save_as, relief="flat", cursor="hand2", bg=BORDER, fg=TEXT, activebackground=ACCENT, activeforeground="#1a1005", font=("Tahoma", 12), pady=10).pack(side="right", fill="x", expand=True, padx=4)
        tk.Button(btns2, text="پرینت / PDF", command=self.print_pdf, relief="flat", cursor="hand2", bg=BORDER, fg=TEXT, activebackground=ACCENT, activeforeground="#1a1005", font=("Tahoma", 12), pady=10).pack(side="right", fill="x", expand=True, padx=4)
        btns3 = tk.Frame(bottom, bg=BG)
        btns3.pack(fill="x", pady=(0, 2))
        tk.Button(btns3, text="پر کردن نمونه", command=self.fill_sample, relief="flat", cursor="hand2", bg=BG, fg="#4dd6ff", activebackground=CARD, font=("Tahoma", 10)).pack(side="right", padx=8)
        tk.Button(btns3, text="پاک کردن همه", command=self.clear_all, relief="flat", cursor="hand2", bg=BG, fg=MUTED, activebackground=CARD, font=("Tahoma", 10)).pack(side="right", padx=8)
        self.status = tk.Label(bottom, text="آماده", font=("Tahoma", 9), bg=BG, fg=MUTED, anchor="e")
        self.status.pack(fill="x", pady=(2, 0))

        mid = tk.Frame(self, bg=BG)
        mid.pack(fill="both", expand=True, padx=22, pady=2)
        self.canvas = tk.Canvas(mid, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(mid, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.scroll_frame = tk.Frame(self.canvas, bg=BG)
        self.win = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self._refresh_scroll())
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.bind_all("<MouseWheel>", self._on_wheel)
        self.bind_all("<Button-4>", self._on_wheel)
        self.bind_all("<Button-5>", self._on_wheel)

        set_box = tk.Frame(self.scroll_frame, bg=CARD)
        set_box.pack(fill="x", pady=(0, 6))
        tk.Label(set_box, text="چیدمان رزومه:", font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="e", padx=14, pady=(8, 2))
        r1 = tk.Frame(set_box, bg=CARD)
        r1.pack(fill="x", padx=10, pady=2)
        tk.Label(r1, text="جهت صفحه:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=6)
        tk.Radiobutton(r1, text="راست‌چین", variable=self.page_dir, value="rtl", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=6)
        tk.Radiobutton(r1, text="چپ‌چین", variable=self.page_dir, value="ltr", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=6)
        r2 = tk.Frame(set_box, bg=CARD)
        r2.pack(fill="x", padx=10, pady=2)
        tk.Label(r2, text="تراز متن:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=6)
        for val, txt in [("auto", "خودکار"), ("right", "راست"), ("center", "وسط"), ("left", "چپ"), ("justify", "میزان")]:
            tk.Radiobutton(r2, text=txt, variable=self.align_mode, value=val, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        r3 = tk.Frame(set_box, bg=CARD)
        r3.pack(fill="x", padx=10, pady=2)
        tk.Label(r3, text="جای عکس:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=6)
        tk.Radiobutton(r3, text="راست", variable=self.photo_side, value="right", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=6)
        tk.Radiobutton(r3, text="چپ", variable=self.photo_side, value="left", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=6)
        tk.Label(r3, text="زبان تیترها:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=(18, 6))
        tk.Radiobutton(r3, text="فارسی", variable=self.lang_var, value="fa", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Radiobutton(r3, text="English", variable=self.lang_var, value="en", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)

        th_box = tk.Frame(self.scroll_frame, bg=CARD)
        th_box.pack(fill="x", pady=(0, 6))
        tk.Label(th_box, text="تم:", font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="e", padx=14, pady=(8, 4))
        grid = tk.Frame(th_box, bg=CARD)
        grid.pack(fill="x", padx=10, pady=(0, 4))
        for i, (name, cfg) in enumerate(THEMES.items()):
            fg_c = "#0f172a" if name in ("مینیمال نوردیک", "ساکورا پاستیلی") else "#ffffff"
            b = tk.Button(grid, text=name, relief="flat", bd=0, cursor="hand2", bg=cfg["accent"], fg=fg_c, activebackground=cfg["dark"], activeforeground="#ffffff", font=("Tahoma", 9, "bold"), padx=8, pady=7, command=lambda n=name: self.select_theme(n))
            b.grid(row=i // 2, column=1 - (i % 2), sticky="ew", padx=4, pady=3)
            grid.grid_columnconfigure(0, weight=1)
            grid.grid_columnconfigure(1, weight=1)
            self.theme_btns[name] = b
        self.theme_desc = tk.Label(th_box, text="", font=("Tahoma", 9), bg=CARD, fg=MUTED, wraplength=600, justify="right")
        self.theme_desc.pack(anchor="e", padx=14, pady=(0, 6))

        photo_row = tk.Frame(self.scroll_frame, bg=CARD)
        photo_row.pack(fill="x", pady=(0, 6))
        tk.Label(photo_row, text="عکس:", font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT).pack(side="right", padx=12, pady=8)
        self.photo_thumb = tk.Label(photo_row, text="", bg=CARD)
        self.photo_thumb.pack(side="right", padx=4)
        self.photo_status = tk.Label(photo_row, text="بدون عکس", font=("Tahoma", 9), bg=CARD, fg=MUTED)
        self.photo_status.pack(side="right", padx=4)
        tk.Button(photo_row, text="حذف", relief="flat", bd=0, cursor="hand2", bg=CARD, fg="#ff5c5c", font=("Tahoma", 9), command=self.remove_photo).pack(side="left", padx=6, pady=6)
        tk.Button(photo_row, text="انتخاب عکس", relief="flat", bd=0, cursor="hand2", bg=BORDER, fg=TEXT, activebackground=ACCENT, font=("Tahoma", 9, "bold"), padx=12, pady=6, command=self.choose_photo).pack(side="left", padx=6, pady=6)

        pers = tk.Frame(self.scroll_frame, bg=CARD)
        pers.pack(fill="x", pady=5)
        tk.Label(pers, text="مشخصات", font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="e", padx=14, pady=(10, 2))
        for label, key in [("نام و نام خانوادگی *", "name"), ("عنوان شغلی / Job Title", "title"), ("ایمیل / Email", "email"), ("تلفن / Phone", "phone")]:
            tk.Label(pers, text=label, font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(anchor="e", padx=14)
            e = tk.Entry(pers, font=("Tahoma", 11), bg=FIELD_BG, fg=TEXT, insertbackground=ACCENT, relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, justify="right")
            e.pack(fill="x", padx=12, pady=(0, 8), ipady=6)
            self.inputs[key] = e
        opt = tk.Frame(pers, bg=CARD)
        opt.pack(fill="x", padx=12, pady=(0, 10))
        tk.Label(opt, text="نمایش در رزومه:", font=("Tahoma", 8), bg=CARD, fg=MUTED).pack(side="right", padx=4)
        tk.Checkbutton(opt, text="عنوان شغلی", variable=self.show_title, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 8)).pack(side="right", padx=4)
        tk.Checkbutton(opt, text="ایمیل", variable=self.show_email, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 8)).pack(side="right", padx=4)
        tk.Checkbutton(opt, text="تلفن", variable=self.show_phone, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 8)).pack(side="right", padx=4)

        about_box = tk.Frame(self.scroll_frame, bg=CARD)
        about_box.pack(fill="x", pady=5)
        ah = tk.Frame(about_box, bg=CARD)
        ah.pack(fill="x")
        tk.Checkbutton(ah, text="درباره من — نمایش بده", variable=self.show_about, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(ah, text="پاک کردن متن", relief="flat", bd=0, cursor="hand2", bg=CARD, fg=MUTED, font=("Tahoma", 8), command=lambda: self.about_text.delete("1.0", "end")).pack(side="left", padx=10)
        self.about_text = tk.Text(about_box, height=3, font=("Tahoma", 10), bg=FIELD_BG, fg=TEXT, insertbackground=ACCENT, relief="flat", padx=8, pady=6, highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, wrap="word")
        self.about_text.pack(fill="x", padx=12, pady=(0, 12))

        skill_box = tk.Frame(self.scroll_frame, bg=CARD)
        skill_box.pack(fill="x", pady=5)
        sh = tk.Frame(skill_box, bg=CARD)
        sh.pack(fill="x")
        tk.Checkbutton(sh, text="مهارت‌ها — نمایش بده", variable=self.show_skills, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(sh, text="＋ افزودن مهارت", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", font=("Tahoma", 9, "bold"), padx=10, pady=4, command=lambda: self.add_skill("")).pack(side="left", padx=10, pady=(8, 2))
        sk_lay = tk.Frame(skill_box, bg=CARD)
        sk_lay.pack(fill="x", padx=12, pady=(0, 2))
        tk.Label(sk_lay, text="چیدمان مهارت‌ها:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=6)
        tk.Radiobutton(sk_lay, text="ردیفی (یک ردیف)", variable=self.skill_layout, value="row", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Radiobutton(sk_lay, text="ستونی (زیر هم)", variable=self.skill_layout, value="col", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Label(sk_lay, text="استایل:", font=("Tahoma", 9), bg=CARD, fg=MUTED).pack(side="right", padx=(14, 6))
        tk.Radiobutton(sk_lay, text="کپسولی", variable=self.skill_style, value="capsule", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Radiobutton(sk_lay, text="بدون کپسول", variable=self.skill_style, value="plain", bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 9)).pack(side="right", padx=4)
        tk.Label(skill_box, text="هر مهارت یک ردیف جدا — با ✕ کمش کن", font=("Tahoma", 8), bg=CARD, fg=MUTED).pack(anchor="e", padx=14)
        self.skills_container = tk.Frame(skill_box, bg=CARD)
        self.skills_container.pack(fill="x", pady=(0, 8))

        exp_box = tk.Frame(self.scroll_frame, bg=CARD)
        exp_box.pack(fill="x", pady=5)
        eh = tk.Frame(exp_box, bg=CARD)
        eh.pack(fill="x")
        tk.Checkbutton(eh, text="سوابق کاری — نمایش بده", variable=self.show_exp, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(eh, text="＋ افزودن سابقه", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", font=("Tahoma", 9, "bold"), padx=10, pady=4, command=lambda: self.add_exp("", "")).pack(side="left", padx=10, pady=(8, 2))
        self.exp_container = tk.Frame(exp_box, bg=CARD)
        self.exp_container.pack(fill="x", pady=(0, 8))

        edu_box = tk.Frame(self.scroll_frame, bg=CARD)
        edu_box.pack(fill="x", pady=5)
        dh = tk.Frame(edu_box, bg=CARD)
        dh.pack(fill="x")
        tk.Checkbutton(dh, text="تحصیلات — نمایش بده", variable=self.show_edu, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(dh, text="＋ افزودن تحصیل", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", font=("Tahoma", 9, "bold"), padx=10, pady=4, command=lambda: self.add_edu("", "")).pack(side="left", padx=10, pady=(8, 2))
        self.edu_container = tk.Frame(edu_box, bg=CARD)
        self.edu_container.pack(fill="x", pady=(0, 8))

        link_box = tk.Frame(self.scroll_frame, bg=CARD)
        link_box.pack(fill="x", pady=5)
        lh = tk.Frame(link_box, bg=CARD)
        lh.pack(fill="x")
        tk.Checkbutton(lh, text="لینک‌ها — نمایش بده", variable=self.show_links, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(lh, text="＋ افزودن لینک", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", font=("Tahoma", 9, "bold"), padx=10, pady=4, command=lambda: self.add_link("", "")).pack(side="left", padx=10, pady=(8, 2))
        tk.Label(link_box, text="گیت‌هاب، لینکدین، سایت، نمونه‌کار...", font=("Tahoma", 8), bg=CARD, fg=MUTED).pack(anchor="e", padx=14)
        self.link_container = tk.Frame(link_box, bg=CARD)
        self.link_container.pack(fill="x", pady=(0, 8))

        cert_box = tk.Frame(self.scroll_frame, bg=CARD)
        cert_box.pack(fill="x", pady=5)
        ch = tk.Frame(cert_box, bg=CARD)
        ch.pack(fill="x")
        tk.Checkbutton(ch, text="گواهی‌ها و مدارک — نمایش بده", variable=self.show_certs, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 10, "bold")).pack(side="right", padx=10, pady=(10, 2))
        tk.Button(ch, text="＋ افزودن مدرک", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", font=("Tahoma", 9, "bold"), padx=10, pady=4, command=lambda: self.add_cert("", "")).pack(side="left", padx=10, pady=(8, 2))
        tk.Label(cert_box, text="مدرک، سرتیفیکیت، دوره... — با ✕ کمش کن", font=("Tahoma", 8), bg=CARD, fg=MUTED).pack(anchor="e", padx=14)
        self.cert_container = tk.Frame(cert_box, bg=CARD)
        self.cert_container.pack(fill="x", pady=(0, 8))

        custom_head = tk.Frame(self.scroll_frame, bg=BG)
        custom_head.pack(fill="x", pady=(10, 4))
        tk.Button(custom_head, text="＋ افزودن بخش جدید (پروژه، زبان، افتخار...)", relief="flat", bd=0, cursor="hand2", bg=ACCENT, fg="#1a1005", activebackground=ACCENT_DARK, font=("Tahoma", 10, "bold"), padx=14, pady=9, command=lambda: self.add_section("", "")).pack(fill="x")
        self.custom_container = tk.Frame(self.scroll_frame, bg=BG)
        self.custom_container.pack(fill="x")

        self.select_theme("زمرد مدرن")
        self.add_skill("")
        self.add_skill("")
        self.add_exp("", "")
        self.add_edu("", "")
        self.add_cert("", "")
        self.add_link("", "")
        self._closing = False
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self._closing = True
        try:
            self.destroy()
        except Exception:
            pass

    def _after_ui(self):
        try:
            if getattr(self, "_closing", False):
                return
            self.after(50, self._refresh_scroll)
        except Exception:
            pass

    def _on_wheel(self, event):
        try:
            if getattr(self, "_closing", False):
                return None
            num = getattr(event, "num", None)
            if num == 4:
                self.canvas.yview_scroll(-1, "units")
                return "break"
            elif num == 5:
                self.canvas.yview_scroll(1, "units")
                return "break"
            else:
                d = getattr(event, "delta", 0)
                if d:
                    self.canvas.yview_scroll(-int(d / 120), "units")
                    return "break"
        except Exception:
            pass
        return None

    def _refresh_scroll(self):
        try:
            if getattr(self, "_closing", False):
                return
            self.update_idletasks()
            box = self.canvas.bbox("all")
            if box:
                self.canvas.configure(scrollregion=box)
        except Exception:
            pass

    def select_theme(self, name):
        try:
            self.theme_name.set(name)
            cfg = THEMES.get(name, list(THEMES.values())[0])
            self.theme_desc.config(text=cfg.get("desc", ""))
            for n, b in self.theme_btns.items():
                try:
                    b.config(relief="solid" if n == name else "flat", bd=2 if n == name else 0)
                except Exception:
                    pass
            self.set_status("تم: " + name)
        except Exception:
            pass

    def _update_photo_thumb(self):
        try:
            if self.photo_path and HAS_PIL and HAS_IMAGETK and os.path.exists(self.photo_path):
                im = Image.open(self.photo_path)
                try:
                    im = ImageOps.exif_transpose(im)
                except Exception:
                    pass
                im.thumbnail((52, 52), Image.LANCZOS)
                self.photo_thumb_img = ImageTk.PhotoImage(im)
                self.photo_thumb.config(image=self.photo_thumb_img, text="")
            elif self.photo_data_uri:
                self.photo_thumb.config(image="", text="✓")
            else:
                self.photo_thumb.config(image="", text="")
                self.photo_thumb_img = None
        except Exception:
            pass

    def choose_photo(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.webp *.bmp"), ("All", "*.*")])
            if not path:
                return
            uri, size = image_file_to_datauri(path, max_dim=512, quality=85)
            self.photo_data_uri = uri
            self.photo_path = path
            base = os.path.basename(path)
            if len(base) > 26:
                base = base[:23] + "..."
            kb = int(size / 1024)
            self.photo_status.config(text="✓ " + base + f" ({kb}KB)", fg="#39ff8b")
            self._update_photo_thumb()
            self.set_status("عکس انتخاب شد و بهینه شد")
            self._after_ui()
        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("خطا", str(ex))

    def remove_photo(self):
        self.photo_path = None
        self.photo_data_uri = None
        self.photo_thumb_img = None
        try:
            self.photo_thumb.config(image="", text="")
            self.photo_status.config(text="بدون عکس", fg=MUTED)
        except Exception:
            pass

    def add_skill(self, value=""):
        try:
            row = tk.Frame(self.skills_container, bg=CARD)
            row.pack(fill="x", padx=12, pady=3)
            bdel = tk.Button(row, text="✕ کم کن", relief="flat", bd=0, cursor="hand2", bg=CARD, fg="#ff5c5c", font=("Tahoma", 8, "bold"), command=lambda: self._del_skill(row))
            bdel.pack(side="left", padx=4)
            e = tk.Entry(row, font=("Tahoma", 10), bg=FIELD_BG, fg=TEXT, insertbackground=ACCENT, relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, justify="right")
            e.pack(side="right", fill="x", expand=True, ipady=6)
            if value:
                e.insert(0, value)
            self.skill_items.append({"frame": row, "entry": e})
            self._after_ui()
        except Exception:
            traceback.print_exc()

    def _del_skill(self, row):
        try:
            for i, s in enumerate(list(self.skill_items)):
                if s["frame"] == row:
                    try:
                        s["frame"].destroy()
                    except Exception:
                        pass
                    self.skill_items.pop(i)
                    break
            self._after_ui()
        except Exception:
            pass

    def _make_double_box(self, container, lst, kind, title="", desc=""):
        try:
            box = tk.Frame(container, bg=FIELD_BG, highlightthickness=1, highlightbackground=BORDER)
            box.pack(fill="x", padx=12, pady=5)
            top = tk.Frame(box, bg=FIELD_BG)
            top.pack(fill="x")
            tk.Label(top, text=kind, font=("Tahoma", 8, "bold"), bg=FIELD_BG, fg=MUTED).pack(side="right", padx=8, pady=(6, 0))
            btns = tk.Frame(top, bg=FIELD_BG)
            btns.pack(side="left", padx=4)
            tk.Button(btns, text="✕", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg="#ff5c5c", font=("Tahoma", 8, "bold"), command=lambda: self._del_item(lst, box)).pack(side="left", padx=2)
            tk.Button(btns, text="▲", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_item(lst, container, box, -1)).pack(side="left", padx=2)
            tk.Button(btns, text="▼", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_item(lst, container, box, 1)).pack(side="left", padx=2)
            te = tk.Entry(box, font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT, insertbackground=ACCENT, relief="flat", justify="right")
            te.pack(fill="x", padx=8, pady=4, ipady=5)
            if title:
                te.insert(0, title)
            td = tk.Text(box, height=2, font=("Tahoma", 10), bg=CARD, fg=TEXT, insertbackground=ACCENT, relief="flat", padx=8, pady=4, wrap="word")
            td.pack(fill="x", padx=8, pady=(0, 8))
            if desc:
                td.insert("1.0", desc)
            lst.append({"frame": box, "title": te, "desc": td})
            self._after_ui()
        except Exception:
            traceback.print_exc()

    def add_exp(self, title="", desc=""):
        self._make_double_box(self.exp_container, self.exp_items, "سابقه", title, desc)

    def add_edu(self, title="", desc=""):
        self._make_double_box(self.edu_container, self.edu_items, "تحصیل", title, desc)

    def add_cert(self, title="", desc=""):
        self._make_double_box(self.cert_container, self.cert_items, "مدرک", title, desc)

    def add_link(self, title="", url=""):
        try:
            box = tk.Frame(self.link_container, bg=FIELD_BG, highlightthickness=1, highlightbackground=BORDER)
            box.pack(fill="x", padx=12, pady=5)
            top = tk.Frame(box, bg=FIELD_BG)
            top.pack(fill="x")
            tk.Label(top, text="لینک", font=("Tahoma", 8, "bold"), bg=FIELD_BG, fg=MUTED).pack(side="right", padx=8, pady=(6, 0))
            btns = tk.Frame(top, bg=FIELD_BG)
            btns.pack(side="left", padx=4)
            tk.Button(btns, text="✕", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg="#ff5c5c", font=("Tahoma", 8, "bold"), command=lambda: self._del_item(self.link_items, box)).pack(side="left", padx=2)
            tk.Button(btns, text="▲", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_item(self.link_items, self.link_container, box, -1)).pack(side="left", padx=2)
            tk.Button(btns, text="▼", relief="flat", bd=0, cursor="hand2", bg=FIELD_BG, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_item(self.link_items, self.link_container, box, 1)).pack(side="left", padx=2)
            tk.Label(box, text="عنوان لینک:", font=("Tahoma", 8), bg=FIELD_BG, fg=MUTED).pack(anchor="e", padx=8)
            te = tk.Entry(box, font=("Tahoma", 10, "bold"), bg=CARD, fg=TEXT, insertbackground=ACCENT, relief="flat", justify="right")
            te.pack(fill="x", padx=8, pady=2, ipady=5)
            if title:
                te.insert(0, title)
            tk.Label(box, text="آدرس لینک:", font=("Tahoma", 8), bg=FIELD_BG, fg=MUTED).pack(anchor="e", padx=8)
            ue = tk.Entry(box, font=("Tahoma", 10), bg=CARD, fg="#7dd3fc", insertbackground=ACCENT, relief="flat", justify="left")
            ue.pack(fill="x", padx=8, pady=(0, 8), ipady=5)
            if url:
                ue.insert(0, url)
            self.link_items.append({"frame": box, "title": te, "url": ue})
            self._after_ui()
        except Exception:
            traceback.print_exc()

    def _del_item(self, lst, box):
        try:
            for i, s in enumerate(list(lst)):
                if s["frame"] == box:
                    try:
                        s["frame"].destroy()
                    except Exception:
                        pass
                    lst.pop(i)
                    break
            self._after_ui()
        except Exception:
            pass

    def _move_item(self, lst, container, box, direction):
        try:
            idx = None
            for i, s in enumerate(lst):
                if s["frame"] == box:
                    idx = i
                    break
            if idx is None:
                return
            j = idx + direction
            if j < 0 or j >= len(lst):
                return
            lst[idx], lst[j] = lst[j], lst[idx]
            for s in lst:
                try:
                    s["frame"].pack_forget()
                except Exception:
                    pass
            for s in lst:
                try:
                    s["frame"].pack(fill="x", padx=12, pady=5)
                except Exception:
                    pass
            self._after_ui()
        except Exception:
            pass

    def add_section(self, title="", content=""):
        try:
            box = tk.Frame(self.custom_container, bg=CARD)
            box.pack(fill="x", pady=5)
            top = tk.Frame(box, bg=CARD)
            top.pack(fill="x")
            show_var = tk.BooleanVar(value=True)
            tk.Checkbutton(top, text="نمایش", variable=show_var, bg=CARD, fg=TEXT, selectcolor=BG, activebackground=CARD, font=("Tahoma", 8)).pack(side="right", padx=8, pady=(8, 0))
            tk.Label(top, text="بخش سفارشی", font=("Tahoma", 9, "bold"), bg=CARD, fg=TEXT).pack(side="right", padx=4, pady=(8, 0))
            btns = tk.Frame(top, bg=CARD)
            btns.pack(side="left", padx=6, pady=(8, 0))
            tk.Button(btns, text="✕ حذف", relief="flat", bd=0, cursor="hand2", bg=CARD, fg="#ff5c5c", font=("Tahoma", 8), command=lambda: self._del_custom(box)).pack(side="left", padx=2)
            tk.Button(btns, text="▲", relief="flat", bd=0, cursor="hand2", bg=CARD, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_custom(box, -1)).pack(side="left", padx=2)
            tk.Button(btns, text="▼", relief="flat", bd=0, cursor="hand2", bg=CARD, fg=MUTED, font=("Tahoma", 8), command=lambda: self._move_custom(box, 1)).pack(side="left", padx=2)
            title_entry = tk.Entry(box, font=("Tahoma", 11, "bold"), bg=FIELD_BG, fg=TEXT, insertbackground=ACCENT, relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, justify="right")
            title_entry.pack(fill="x", padx=12, pady=(4, 4), ipady=6)
            if title:
                title_entry.insert(0, title)
            content_text = tk.Text(box, height=3, font=("Tahoma", 10), bg=FIELD_BG, fg=TEXT, insertbackground=ACCENT, relief="flat", padx=8, pady=6, highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, wrap="word")
            content_text.pack(fill="x", padx=12, pady=(0, 12))
            if content:
                content_text.insert("1.0", content)
            self.custom_sections.append({"frame": box, "show": show_var, "title": title_entry, "content": content_text})
            try:
                title_entry.focus()
            except Exception:
                pass
            self._after_ui()
            self.set_status("بخش جدید اضافه شد — با ✕ کمش کن")
        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("خطا", str(ex))

    def _del_custom(self, box):
        try:
            for i, s in enumerate(list(self.custom_sections)):
                if s["frame"] == box:
                    try:
                        s["frame"].destroy()
                    except Exception:
                        pass
                    self.custom_sections.pop(i)
                    break
            self._after_ui()
        except Exception:
            pass

    def _move_custom(self, box, direction):
        try:
            idx = None
            for i, s in enumerate(self.custom_sections):
                if s["frame"] == box:
                    idx = i
                    break
            if idx is None:
                return
            j = idx + direction
            if j < 0 or j >= len(self.custom_sections):
                return
            self.custom_sections[idx], self.custom_sections[j] = self.custom_sections[j], self.custom_sections[idx]
            for s in self.custom_sections:
                try:
                    s["frame"].pack_forget()
                except Exception:
                    pass
            for s in self.custom_sections:
                try:
                    s["frame"].pack(fill="x", pady=5)
                except Exception:
                    pass
        except Exception:
            pass

    def set_status(self, text, color=None):
        try:
            self.status.config(text=text, fg=color or MUTED)
        except Exception:
            pass

    def get_val(self, key):
        try:
            return self.inputs[key].get().strip()
        except Exception:
            return ""

    def _settings(self):
        return {"page_dir": self.page_dir.get() or "rtl", "align": self.align_mode.get() or "auto", "photo_side": self.photo_side.get() or "right", "lang": self.lang_var.get() or "fa", "skill_layout": self.skill_layout.get() or "row", "skill_style": self.skill_style.get() or "capsule"}

    def _item_html(self, title, desc, page_dir, align_mode):
        t = (title or "").strip()
        d = (desc or "").strip()
        if not t and not d:
            return ""
        if t.strip() in ("-", "—", "--") and not d:
            return ""
        th = ""
        if t and t not in ("-", "—", "--"):
            if align_mode == "auto":
                rtl = is_fa(t)
                dd = "rtl" if rtl else "ltr"
                aa = "right" if rtl else "left"
            else:
                dd = page_dir
                aa = align_mode if align_mode in ("right", "left", "center") else ("right" if page_dir == "rtl" else "left")
            th = '<div class="exp-title" dir="' + dd + '" style="text-align:' + aa + ';">' + html.escape(t) + '</div>'
        dh = render_paragraphs(d, page_dir, align_mode) if d else ""
        if not th and not dh:
            return ""
        return '<div class="exp-item">' + th + dh + '</div>'

    def _cert_html(self, title, desc, page_dir, align_mode):
        t = (title or "").strip()
        d = (desc or "").strip()
        if not t and not d:
            return ""
        if t in ("-", "—", "--") and not d:
            return ""
        if align_mode == "auto":
            rtl = is_fa(t) if t else False
            dd = "rtl" if rtl else "ltr"
            aa = "right" if rtl else "left"
        else:
            dd = page_dir
            aa = align_mode if align_mode in ("right", "left", "center") else ("right" if page_dir == "rtl" else "left")
        inner = ""
        if t and t not in ("-", "—", "--"):
            inner += '<div class="exp-title" dir="' + dd + '" style="text-align:' + aa + ';">' + html.escape(t) + '</div>'
        if d:
            inner += render_paragraphs(d, page_dir, align_mode)
        if not inner:
            return ""
        return '<div class="exp-item">' + inner + '</div>'

    def _link_html(self, title, url, page_dir, align_mode):
        t = (title or "").strip()
        u = (url or "").strip()
        if not t and not u:
            return ""
        if t in ("-", "—") and not u:
            return ""
        if u in ("-", "—", "--"):
            return ""
        if not u:
            return self._item_html(t, "", page_dir, align_mode)
        href = u
        if " " not in href and "://" not in href and "." in href:
            href = "https://" + href
        disp_t = html.escape(t) if t else html.escape(u)
        if align_mode == "auto":
            rtl = is_fa(t) if t else False
            dd = "rtl" if rtl else "ltr"
            aa = "right" if rtl else "left"
        else:
            dd = page_dir
            aa = align_mode if align_mode in ("right", "left", "center") else ("right" if page_dir == "rtl" else "left")
        return '<div class="exp-item" dir="' + dd + '" style="text-align:' + aa + ';"><div class="exp-title">' + disp_t + '</div><div class="body" dir="ltr" style="text-align:left;"><a class="link-a" href="' + html.escape(href, quote=True) + '" target="_blank">' + html.escape(u) + '</a></div></div>'

    def _build_html(self):
        data_name = self.get_val("name").strip()
        if not data_name:
            return None
        st = self._settings()
        page_dir = st["page_dir"]
        align_mode = st["align"]
        photo_side = st["photo_side"]
        lang = st["lang"]
        skill_layout = st["skill_layout"]
        lab = LABELS.get(lang, LABELS["fa"])
        cfg = THEMES.get(self.theme_name.get(), list(THEMES.values())[0])

        if self.photo_data_uri:
            photo_html = '<img class="avatar-img" src="' + self.photo_data_uri + '" alt="photo">'
        else:
            photo_html = '<div class="avatar">' + html.escape(data_name.strip()[0]) + '</div>'

        try:
            show_t = bool(self.show_title.get())
        except Exception:
            show_t = True
        try:
            show_e = bool(self.show_email.get())
        except Exception:
            show_e = True
        try:
            show_p = bool(self.show_phone.get())
        except Exception:
            show_p = True

        if align_mode == "auto":
            rtl_n = is_fa(data_name)
            dn = "rtl" if rtl_n else "ltr"
            an = "right" if rtl_n else "left"
            name_h = '<h1 dir="' + dn + '" style="text-align:' + an + ';">' + html.escape(data_name) + '</h1>'
            title_raw = self.get_val("title").strip()
            if show_t and title_raw and title_raw not in ("-", "—"):
                rtl_t = is_fa(title_raw)
                dt = "rtl" if rtl_t else "ltr"
                at = "right" if rtl_t else "left"
                title_h = '<div class="hero-sub" dir="' + dt + '" style="text-align:' + at + ';">' + html.escape(title_raw) + '</div>'
            else:
                title_h = ""
        else:
            ha = align_mode if align_mode in ("right", "left", "center") else ("right" if page_dir == "rtl" else "left")
            name_h = '<h1 dir="' + page_dir + '" style="text-align:' + ha + ';">' + html.escape(data_name) + '</h1>'
            title_raw = self.get_val("title").strip()
            if show_t and title_raw and title_raw not in ("-", "—"):
                title_h = '<div class="hero-sub" dir="' + page_dir + '" style="text-align:' + ha + ';">' + html.escape(title_raw) + '</div>'
            else:
                title_h = ""

        if align_mode == "center":
            contact_align = "center"
        elif align_mode in ("right", "left"):
            contact_align = align_mode
        else:
            contact_align = "right" if page_dir == "rtl" else "left"
        parts = []
        if show_e:
            ev = self.get_val("email").strip()
            if ev and ev not in ("-", "—"):
                parts.append(html.escape(ev))
        if show_p:
            pv = self.get_val("phone").strip()
            if pv and pv not in ("-", "—"):
                parts.append(html.escape(pv))
        if parts:
            contact_h = '<div class="hero-sub" dir="ltr" style="text-align:' + contact_align + ';">' + " &nbsp;|&nbsp; ".join(parts) + '</div>'
        else:
            contact_h = ""
        info_h = '<div style="flex:1;min-width:240px;">' + name_h + title_h + contact_h + '</div>'
        photo_first = (page_dir == "rtl" and photo_side == "right") or (page_dir == "ltr" and photo_side == "left")
        hero_inner = (photo_html + info_h) if photo_first else (info_h + photo_html)

        sections = ""
        if self.show_about.get():
            a = head_align(lab["about"], page_dir, align_mode)
            about_t = self.about_text.get("1.0", "end").strip()
            about_h = render_paragraphs(about_t, page_dir, align_mode)
            if about_h:
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["about"] + '</h2></div>' + about_h + '</div>'
        if self.show_skills.get():
            a = head_align(lab["skills"], page_dir, align_mode)
            vals = []
            for s in self.skill_items:
                try:
                    v = s["entry"].get().strip()
                    if v and v not in ("-", "—", "--"):
                        vals.append(v)
                except Exception:
                    continue
            if vals:
                if align_mode == "center":
                    sk_a = "center"
                elif align_mode in ("right", "left"):
                    sk_a = align_mode
                else:
                    sk_a = "right" if page_dir == "rtl" else "left"
                skill_style = st.get("skill_style", "capsule")
                if skill_style == "plain":
                    if skill_layout == "col":
                        tags = "".join('<div style="margin:3px 0;"><span class="tag-plain" dir="auto">' + html.escape(v) + "</span></div>" for v in vals)
                    else:
                        tags = '<span class="tag-sep">•</span>'.join('<span class="tag-plain" dir="auto">' + html.escape(v) + "</span>" for v in vals)
                else:
                    if skill_layout == "col":
                        tags = "".join('<div style="margin:3px 0;"><span class="tag" dir="auto">' + html.escape(v) + "</span></div>" for v in vals)
                    else:
                        tags = " ".join('<span class="tag" dir="auto">' + html.escape(v) + "</span>" for v in vals)
                body = '<div dir="' + page_dir + '" style="text-align:' + sk_a + ';">' + tags + '</div>'
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["skills"] + '</h2></div><div>' + body + '</div></div>'
        if self.show_exp.get():
            a = head_align(lab["exp"], page_dir, align_mode)
            items_h = ""
            for it in self.exp_items:
                try:
                    t = it["title"].get().strip()
                    d = it["desc"].get("1.0", "end").strip()
                    h = self._item_html(t, d, page_dir, align_mode)
                    if h:
                        items_h += h
                except Exception:
                    continue
            if items_h:
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["exp"] + '</h2></div>' + items_h + '</div>'
        if self.show_edu.get():
            a = head_align(lab["edu"], page_dir, align_mode)
            items_h = ""
            for it in self.edu_items:
                try:
                    t = it["title"].get().strip()
                    d = it["desc"].get("1.0", "end").strip()
                    h = self._item_html(t, d, page_dir, align_mode)
                    if h:
                        items_h += h
                except Exception:
                    continue
            if items_h:
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["edu"] + '</h2></div>' + items_h + '</div>'
        try:
            show_l = bool(self.show_links.get())
        except Exception:
            show_l = True
        if show_l:
            a = head_align(lab["links"], page_dir, align_mode)
            items_h = ""
            for it in self.link_items:
                try:
                    t = it["title"].get().strip()
                    u = it["url"].get().strip()
                    h = self._link_html(t, u, page_dir, align_mode)
                    if h:
                        items_h += h
                except Exception:
                    continue
            if items_h:
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["links"] + '</h2></div>' + items_h + '</div>'
        for s in self.custom_sections:
            try:
                try:
                    show = s["show"].get()
                except Exception:
                    show = True
                if not show:
                    continue
                t = s["title"].get().strip() or "بخش اضافه"
                c = s["content"].get("1.0", "end").strip()
                if not c and not s["title"].get().strip():
                    continue
                rh = render_paragraphs(c, page_dir, align_mode)
                if not rh and not s["title"].get().strip():
                    continue
                a = head_align(t, page_dir, align_mode)
                if rh:
                    sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + html.escape(t) + '</h2></div>' + rh + '</div>'
                elif t:
                    sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + html.escape(t) + '</h2></div></div>'
            except Exception:
                continue
        try:
            show_c = bool(self.show_certs.get())
        except Exception:
            show_c = True
        if show_c:
            a = head_align(lab["certs"], page_dir, align_mode)
            items_h = ""
            for it in self.cert_items:
                try:
                    t = it["title"].get().strip()
                    d = it["desc"].get("1.0", "end").strip()
                    h = self._cert_html(t, d, page_dir, align_mode)
                    if h:
                        items_h += h
                except Exception:
                    continue
            if items_h:
                sections += '<div class="card"><div class="h2-wrap" style="text-align:' + a + ';"><h2>' + lab["certs"] + '</h2></div>' + items_h + '</div>'

        out = TEMPLATE
        out = out.replace("__LANG__", lab["lang"])
        out = out.replace("__PAGE_DIR__", page_dir)
        out = out.replace("__HERO_BG__", cfg["hero_bg"])
        out = out.replace("__HERO_TEXT__", cfg["hero_text"])
        out = out.replace("__H2__", cfg["h2"])
        out = out.replace("__TAG_BG__", cfg["tag_bg"])
        out = out.replace("__TAG_FG__", cfg["tag_fg"])
        out = out.replace("__TAG_BORDER__", cfg["tag_border"])
        out = out.replace("__HERO_INNER__", hero_inner)
        out = out.replace("__NAME__", html.escape(data_name))
        out = out.replace("__FOOTER__", lab["footer"])
        out = out.replace("__SECTIONS__", sections)
        return out

    def _write_temp(self, html_text):
        tmp = tempfile.gettempdir()
        path = os.path.join(tmp, "resume_preview.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_text)
        return os.path.abspath(path)

    def _open_browser(self, path):
        uri = pathlib.Path(path).as_uri()
        webbrowser.open(uri)

    def preview(self):
        try:
            h = self._build_html()
            if not h:
                messagebox.showwarning("خطا", "نام و نام خانوادگی را وارد کنید.")
                return
            p = self._write_temp(h)
            self._open_browser(p)
            self.set_status("پیش‌نمایش باز شد", "#39ff8b")
        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("خطا", "خطا در پیش‌نمایش:\n" + str(ex))

    def save_as(self):
        try:
            h = self._build_html()
            if not h:
                messagebox.showwarning("خطا", "نام و نام خانوادگی را وارد کنید.")
                return
            path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")], initialfile="resume.html")
            if not path:
                return
            with open(path, "w", encoding="utf-8") as f:
                f.write(h)
            messagebox.showinfo("موفق", "رزومه ذخیره شد:\n" + path)
            self.set_status("ذخیره شد", "#39ff8b")
        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("خطا", str(ex))

    def print_pdf(self):
        try:
            h = self._build_html()
            if not h:
                messagebox.showwarning("خطا", "نام و نام خانوادگی را وارد کنید.")
                return
            p = self._write_temp(h)
            self._open_browser(p)
            messagebox.showinfo("پرینت", "صفحه در مرورگر باز شد. کلید Ctrl+P را بزنید و Save as PDF را انتخاب کنید.")
        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("خطا", str(ex))

    def _clear_list(self, lst):
        for it in list(lst):
            try:
                it["frame"].destroy()
            except Exception:
                pass
        lst.clear()

    def fill_sample(self):
        try:
            self.inputs["name"].delete(0, "end")
            self.inputs["name"].insert(0, "Aria")
            self.inputs["title"].delete(0, "end")
            self.inputs["title"].insert(0, "Backend Developer")
            self.inputs["email"].delete(0, "end")
            self.inputs["email"].insert(0, "aria@example.com")
            self.inputs["phone"].delete(0, "end")
            self.inputs["phone"].insert(0, "09120000000")
            self.about_text.delete("1.0", "end")
            self.about_text.insert("1.0", "Backend developer with 3 years of experience.")
            self._clear_list(self.skill_items)
            for v in ["Python", "Django / FastAPI", "Git & Docker", "SQL"]:
                self.add_skill(v)
            self._clear_list(self.exp_items)
            self.add_exp("Backend Developer - Sample Co.", "Built shop website.")
            self.add_exp("Freelancer", "Made 5 desktop apps.")
            self._clear_list(self.edu_items)
            self.add_edu("B.Sc. Software Engineering", "2019 - 2023")
            self._clear_list(self.cert_items)
            self.add_cert("Python Certificate - Sample", "2023")
            self._clear_list(self.link_items)
            self.add_link("GitHub", "github.com/aria")
            self.add_link("LinkedIn", "linkedin.com/in/aria")
            if not self.custom_sections:
                self.add_section("Languages", "English (Intermediate)")
            self.set_status("نمونه پر شد", "#4dd6ff")
        except Exception:
            traceback.print_exc()

    def clear_all(self):
        try:
            for k in self.inputs:
                try:
                    self.inputs[k].delete(0, "end")
                except Exception:
                    pass
            try:
                self.about_text.delete("1.0", "end")
            except Exception:
                pass
            self._clear_list(self.skill_items)
            self.add_skill("")
            self._clear_list(self.exp_items)
            self.add_exp("", "")
            self._clear_list(self.edu_items)
            self.add_edu("", "")
            self._clear_list(self.cert_items)
            self.add_cert("", "")
            self._clear_list(self.link_items)
            self.add_link("", "")
            for s in list(self.custom_sections):
                try:
                    s["frame"].destroy()
                except Exception:
                    pass
            self.custom_sections.clear()
            self.set_status("پاک شد", MUTED)
        except Exception:
            pass

if __name__ == "__main__":
    try:
        App().mainloop()
    except Exception:
        import traceback as _tb
        _tb.print_exc()
        try:
            messagebox.showerror("خطای بحرانی", _tb.format_exc()[-2000:])
        except Exception:
            pass
