#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path
from filename_utils import clean_name
import tkinter as tk
from tkinter import messagebox, filedialog

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False
    TkinterDnD = None
    DND_FILES = None


# `clean_name` is provided by `filename_utils.py` so tests and other tools
# can import the function without importing tkinter.


class FileRenamerApp:
    """Main application class."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Filename Cleaner")
        self.files: list[Path] = []  # preserve order
        self.file_set = set()
        self.allow_overwrite = tk.IntVar(value=0)
        self._build_ui()

    def _build_ui(self) -> None:
        frm = tk.Frame(self.root, padx=8, pady=8)
        frm.pack(fill=tk.BOTH, expand=True)

        # Instruction / drop area
        self.drop_label = tk.Label(
            frm,
            text=("Drag & drop files here" if DND_AVAILABLE else "Drag & drop not available - use Add Files"),
            relief=tk.RIDGE,
            width=48,
            height=4,
            bg="#f7f7f7",
        )
        self.drop_label.pack(fill=tk.X)

        if DND_AVAILABLE:
            # Register drop handler
            try:
                self.drop_label.drop_target_register(DND_FILES)
                self.drop_label.dnd_bind("<<Drop>>", self.on_drop)
            except Exception:
                # some platforms may still fail; leave label as informational
                pass

        # Preview list with old -> new
        list_frame = tk.Frame(frm)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self.listbox = tk.Listbox(list_frame, height=12, width=100)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Controls
        ctl_frame = tk.Frame(frm)
        ctl_frame.pack(fill=tk.X, pady=(8, 0))

        add_btn = tk.Button(ctl_frame, text="Add Files...", command=self.add_files)
        add_btn.pack(side=tk.LEFT)

        clear_btn = tk.Button(ctl_frame, text="Clear List", command=self.clear_list)
        clear_btn.pack(side=tk.LEFT, padx=6)

        rename_btn = tk.Button(ctl_frame, text="Rename Files", command=self.rename_files)
        rename_btn.pack(side=tk.RIGHT)

        overwrite_cb = tk.Checkbutton(
            ctl_frame,
            text="Allow overwrite (dangerous)",
            variable=self.allow_overwrite,
        )
        overwrite_cb.pack(side=tk.RIGHT, padx=8)

        # Status area
        self.status = tk.Label(self.root, text="Ready", anchor=tk.W)
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
        """Handle files dropped onto the drop label.

        Event.data can contain one or more filenames; use splitlist to
        get them robustly. Ignore directories and duplicates.
        """
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
            self.listbox.insert(tk.END, f"{p.name} \u001E {newname}")
        self.set_status(f"{len(self.files)} file(s) in list — dry-run preview")

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
            summary_lines.append(f"{len(collisions)} target(s) already exist and will be skipped unless overwrite is enabled.")

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
                    # overwrite allowed
                    os.replace(src, dst)
                    renamed += 1
                else:
                    # same path or target does not exist
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
