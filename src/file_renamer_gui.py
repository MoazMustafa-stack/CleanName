#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path
from filename_utils import clean_name
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False
    TkinterDnD = None
    DND_FILES = None

COLOR_BG = "#121212"
COLOR_SURFACE = "#1E1E1E"
COLOR_ACCENT = "#3D7EBF"
COLOR_TEXT = "#E0E0E0"
COLOR_TEXT_SECONDARY = "#A0A0A0"
COLOR_DND = "#252525"

class FileRenamerApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CleanName")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)
        self.center_window()
        
        self.files: list[Path] = []
        self.file_set = set()
        self.allow_overwrite = tk.IntVar(value=0)
        self.bg_image = None
        
        self.setup_ui()

    def center_window(self) -> None:
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")

    def load_background_image(self) -> None:
        asset_path = Path("assets/background.png")
        if asset_path.exists():
            try:
                img = Image.open(asset_path)
                img = img.resize((700, 600), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.bg_label.config(image=self.bg_image)
            except Exception:
                pass

    def setup_ui(self) -> None:
        self.bg_label = tk.Label(self.root, bg=COLOR_BG)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_background_image()
        
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        dnd_frame = tk.Frame(main_frame, bg=COLOR_DND)
        dnd_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        dnd_inner = tk.Frame(dnd_frame, bg=COLOR_DND)
        dnd_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(
            dnd_inner,
            text="Drag & drop files here",
            font=("Arial", 14, "bold"),
            bg=COLOR_DND,
            fg=COLOR_TEXT
        )
        title_label.pack(pady=(0, 8))
        
        subtitle_label = tk.Label(
            dnd_inner,
            text="We'll keep only the clean filename",
            font=("Arial", 10),
            bg=COLOR_DND,
            fg=COLOR_TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 20))
        
        self.dnd_zone = tk.Label(
            dnd_inner,
            text="↓ Drop files here ↓",
            font=("Arial", 12),
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_SECONDARY,
            height=4,
            width=50
        )
        self.dnd_zone.pack(fill=tk.BOTH, expand=True, pady=10)
        
        if DND_AVAILABLE:
            try:
                self.dnd_zone.drop_target_register(DND_FILES)
                self.dnd_zone.dnd_bind("<<Drop>>", self.on_drop)
            except Exception:
                pass
        
        list_frame = tk.Frame(dnd_inner, bg=COLOR_DND)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.listbox = tk.Listbox(
            list_frame,
            height=8,
            width=60,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
            selectmode=tk.NONE,
            border=0,
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        button_frame = tk.Frame(dnd_inner, bg=COLOR_DND)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        add_btn = tk.Button(
            button_frame,
            text="Add Files",
            command=self.add_files,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
            padx=12,
            pady=6,
            border=0,
            cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT, padx=4)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_list,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_SECONDARY,
            padx=12,
            pady=6,
            border=0,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=4)
        
        rename_btn = tk.Button(
            button_frame,
            text="Rename Files",
            command=self.rename_files,
            bg=COLOR_ACCENT,
            fg="#FFFFFF",
            padx=16,
            pady=6,
            border=0,
            cursor="hand2",
            font=("Arial", 10, "bold")
        )
        rename_btn.pack(side=tk.RIGHT, padx=4)
        
        overwrite_cb = tk.Checkbutton(
            button_frame,
            text="Allow overwrite",
            variable=self.allow_overwrite,
            bg=COLOR_DND,
            fg=COLOR_TEXT_SECONDARY,
            selectcolor=COLOR_SURFACE,
            activebackground=COLOR_DND,
            activeforeground=COLOR_TEXT
        )
        overwrite_cb.pack(side=tk.RIGHT, padx=4)
        
        self.status = tk.Label(
            self.root,
            text="Ready",
            anchor=tk.W,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_SECONDARY,
            padx=10,
            pady=4
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def set_status(self, text: str) -> None:
        self.status.config(text=text)

    def add_files(self) -> None:
        paths = filedialog.askopenfilenames(title="Select files to add")
        for p in paths:
            self._add_path(Path(p))
        self._refresh_listbox()

    def _add_path(self, p: Path) -> None:
        if not p.exists():
            return
        if p.is_dir():
            return
        resolved = str(p.resolve())
        if resolved in self.file_set:
            return
        self.files.append(p)
        self.file_set.add(resolved)

    def on_drop(self, event) -> None:
        try:
            items = self.root.tk.splitlist(event.data)
        except Exception:
            items = [event.data]

        for it in items:
            p = Path(it)
            self._add_path(p)

        self._refresh_listbox()

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        for p in self.files:
            newname = clean_name(p.name)
            self.listbox.insert(tk.END, f"{p.name} → {newname}")
        self.set_status(f"{len(self.files)} file(s) ready — dry-run preview")

    def clear_list(self) -> None:
        self.files.clear()
        self.file_set.clear()
        self._refresh_listbox()

    def rename_files(self) -> None:
        if not self.files:
            messagebox.showinfo("Nothing to rename", "No files in list.")
            return

        mappings: list[tuple[Path, Path]] = []
        collisions = []
        for p in self.files:
            newname = clean_name(p.name)
            target = p.with_name(newname)
            mappings.append((p, target))
            if target.exists() and str(target.resolve()) != str(p.resolve()):
                collisions.append(target)

        summary_lines = [f"{len(mappings)} files will be processed."]
        if collisions and not self.allow_overwrite.get():
            summary_lines.append(f"{len(collisions)} target(s) already exist and will be skipped.")

        summary = "\n".join(summary_lines)
        if not messagebox.askyesno("Confirm Rename", f"Proceed with rename?\n\n{summary}"):
            return

        renamed = 0
        skipped = 0
        errors = []

        for src, dst in mappings:
            try:
                if not src.exists():
                    skipped += 1
                    continue
                if dst.exists() and str(dst.resolve()) != str(src.resolve()):
                    if not self.allow_overwrite.get():
                        skipped += 1
                        continue
                    os.replace(src, dst)
                    renamed += 1
                else:
                    if str(dst.resolve()) == str(src.resolve()):
                        skipped += 1
                        continue
                    os.rename(src, dst)
                    renamed += 1
            except Exception as exc:
                errors.append(f"{src.name}: {exc}")

        new_files: list[Path] = []
        new_set = set()
        for src, dst in mappings:
            if dst.exists():
                new_files.append(dst)
                new_set.add(str(dst.resolve()))
            elif src.exists():
                new_files.append(src)
                new_set.add(str(src.resolve()))

        self.files = new_files
        self.file_set = new_set
        self._refresh_listbox()

        msg = f"Renamed: {renamed}\nSkipped: {skipped}"
        if errors:
            msg += "\nErrors:\n" + "\n".join(errors[:10])
        messagebox.showinfo("Rename Complete", msg)


def main() -> None:
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = FileRenamerApp(root)

    if not DND_AVAILABLE:
        app.set_status("tkinterdnd2 not installed — use Add Files button")

    root.mainloop()


if __name__ == "__main__":
    main()
