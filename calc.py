import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
import re
import os
import datetime
import json

UI_STRINGS = {
    "en": {
        "app_title": "Notepad Calculator", "file": "File", "new_tab": "New Tab",
        "open_file": "Open File...", "save": "Save", "save_as": "Save As...",
        "close_tab": "Close Tab", "exit": "Exit", "format": "Format", "font": "Font...",
        "insert_heading": "Insert Numbered Heading", "recalculate_all": "Recalculate All",
        "settings": "Settings", "set_default_dir": "Set Default Directory...", "language": "Language",
        "save_changes_prompt": "Save Changes?",
        "save_changes_message": "Do you want to save changes to {tab_name}?",
        "restart_required_title": "Restart Required",
        "restart_required_message": "Language changes will take effect after restarting the application."
    },
    "zh": {
        "app_title": "计算器笔记本", "file": "文件", "new_tab": "新建标签页",
        "open_file": "打开文件...", "save": "保存", "save_as": "另存为...",
        "close_tab": "关闭标签页", "exit": "退出", "format": "格式", "font": "字体...",
        "insert_heading": "插入编号标题", "recalculate_all": "重新计算全部",
        "settings": "设置", "set_default_dir": "设置默认文件夹...", "language": "语言",
        "save_changes_prompt": "保存更改?",
        "save_changes_message": "是否要将更改保存到 {tab_name}?",
        "restart_required_title": "需要重启",
        "restart_required_message": "语言设置将在程序重启后生效。"
    }
}

class FontDialog(tk.Toplevel):
    def __init__(self, parent, current_font):
        super().__init__(parent)
        self.title("Font")
        self.geometry("400x300")
        self.font_family = tk.StringVar(self, value=current_font[0])
        self.font_size = tk.IntVar(self, value=current_font[1])
        tk.Label(self, text="Font Family:").pack(padx=10, anchor="w")
        family_frame = ttk.Frame(self)
        family_frame.pack(expand=True, fill="both", padx=10)
        self.family_listbox = tk.Listbox(family_frame, selectmode="single", exportselection=False)
        self.family_listbox.pack(side="left", expand=True, fill="both")
        family_scrollbar = ttk.Scrollbar(family_frame, orient="vertical", command=self.family_listbox.yview)
        family_scrollbar.pack(side="right", fill="y")
        self.family_listbox.config(yscrollcommand=family_scrollbar.set)
        font_families = sorted(font.families())
        for f in font_families:
            self.family_listbox.insert("end", f)
        if current_font[0] in font_families:
            idx = font_families.index(current_font[0])
            self.family_listbox.selection_set(idx)
            self.family_listbox.see(idx)
        tk.Label(self, text="Font Size:").pack(padx=10, anchor="w")
        size_entry = ttk.Entry(self, textvariable=self.font_size)
        size_entry.pack(padx=10, fill="x")
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side="left", padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=5)
        self.transient(parent)
        self.grab_set()
        self.result = None
    def on_ok(self):
        selected_family_index = self.family_listbox.curselection()
        if selected_family_index:
            self.font_family.set(self.family_listbox.get(selected_family_index))
        self.result = (self.font_family.get(), self.font_size.get())
        self.destroy()

class CalculatorTab(ttk.Frame):
    def __init__(self, parent, file_path=None, current_font=("Arial", 14)):
        super().__init__(parent)
        self.parent = parent
        self.file_path = file_path
        self.has_unsaved_changes = False
        self.current_font = current_font
        self.text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=self.current_font, undo=True)
        self.text_widget.pack(expand=True, fill='both')
        self.text_widget.bind("<Return>", self.on_enter_pressed)
        self.text_widget.bind("<KeyRelease>", self.on_text_changed)
        self.text_widget.bind("<<Paste>>", self.on_paste)
        self._is_updating = False
        if self.file_path and os.path.exists(self.file_path):
            self.load_file()
    def on_paste(self, event=None):
        self.after(50, self.recalculate_all)
    def recalculate_all(self):
        self._is_updating = True
        cursor_pos = self.text_widget.index(tk.INSERT)
        try:
            total_lines = int(self.text_widget.index(f"{tk.END}-1c").split('.')[0])
            for i in range(1, total_lines + 1):
                line_start, line_end = f"{i}.0", f"{i}.end"
                line_text = self.text_widget.get(line_start, line_end)
                
                if '=' in line_text:
                    recalculated_line = self._recalculate_line(line_text)
                    if recalculated_line != line_text:
                        self.text_widget.delete(line_start, line_end)
                        self.text_widget.insert(line_start, recalculated_line)
        finally:
            self.text_widget.mark_set(tk.INSERT, cursor_pos)
            self._is_updating = False
    def load_file(self):
        with open(self.file_path, "r", encoding="utf-8") as f: self.text_widget.insert("1.0", f.read())
        self.text_widget.edit_modified(False)
        self.has_unsaved_changes = False
    def _evaluate_expression_string(self, expression):
        try:
            expression = expression.strip().rstrip('=')
            translation_table = str.maketrans("％（）＋－＊／", "%()+-*/")
            expression = expression.translate(translation_table)
            expression = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', expression)
            return eval(expression, {"__builtins__": {}}, {})
        except Exception:
            return None
    def _recalculate_line(self, line_text):
        new_line = list(line_text)
        # Find all potential "expression = number" patterns
        # Regex: any characters non-greedily (group 1), equals sign, optional space, a number (group 2)
        # We iterate in reverse to ensure that replacements don't mess up the indices of subsequent matches
        for match in reversed(list(re.finditer(r"(.+?)\s*=\s*(-?[\d\.]+)", line_text))):
            expression_str = match.group(1)
            old_result_str = match.group(2)
            
            new_result = self._evaluate_expression_string(expression_str)
            
            if new_result is not None:
                # Format to avoid trailing .0 for whole numbers
                if new_result == int(new_result):
                    new_result_str = str(int(new_result))
                else:
                    new_result_str = str(new_result)
                
                # Compare as numbers to handle float/int differences (e.g., "50" vs "50.0")
                if float(old_result_str) != float(new_result):
                    start, end = match.span(2) # Get the start/end of the old result part
                    # Replace the old result part in our list representation of the string
                    new_line[start:end] = list(new_result_str)

        return "".join(new_line)

    def on_text_changed(self, event):
        cursor_index = self.text_widget.index(tk.INSERT)
        line_number = cursor_index.split('.')[0]
        line_start, line_end = f"{line_number}.0", f"{line_number}.end"
        
        # --- Live period conversion ---
        current_line = self.text_widget.get(line_start, line_end)
        if '。' in current_line:
            match = re.match(r"^(\s*\d+)", current_line)
            if match and current_line.strip().startswith(match.group(0) + '。'):
                original_cursor_col = int(cursor_index.split('.')[1])
                new_line_content = current_line.replace('。', '.', 1)
                self.text_widget.delete(line_start, line_end)
                self.text_widget.insert(line_start, new_line_content)
                self.text_widget.mark_set(tk.INSERT, f"{line_number}.{original_cursor_col}")
                # Update current_line after modification
                current_line = new_line_content

        if self.text_widget.edit_modified(): self.has_unsaved_changes = True
        if self._is_updating: return
        if event.keysym not in ("BackSpace", "Delete") and len(event.char) == 0: return
        
        # --- Inline recalculation logic ---
        if '=' in current_line:
            self._is_updating = True
            try:
                recalculated_line = self._recalculate_line(current_line)
                if recalculated_line != current_line:
                    original_cursor_col = int(self.text_widget.index(tk.INSERT).split('.')[1])
                    self.text_widget.delete(line_start, line_end)
                    self.text_widget.insert(line_start, recalculated_line)
                    # Try to preserve cursor position
                    self.text_widget.mark_set(tk.INSERT, f"{line_number}.{original_cursor_col}")
            finally:
                self._is_updating = False
    def on_enter_pressed(self, event):
        cursor_index = self.text_widget.index(tk.INSERT)
        line_start, line_end = f"{cursor_index.split('.')[0]}.0", f"{cursor_index.split('.')[0]}.end"
        current_line = self.text_widget.get(line_start, line_end)
        current_line_stripped = current_line.strip()
        match = re.match(r"^(\s*)(\d+)\.\s*(.*)", current_line)
        if match:
            leading_space, number, content = match.groups()
            if not content.strip():
                self.text_widget.delete(line_start, line_end)
                return "break"
            self.text_widget.insert(tk.INSERT, f"\n{leading_space}{int(number) + 1}. ")
            return "break"
        match = re.match(r"^(\s*[\*\-])\s+(.*)", current_line)
        if match:
            prefix, content = match.groups()
            if not content.strip():
                self.text_widget.delete(line_start, line_end)
                return "break"
            self.text_widget.insert(tk.INSERT, f"\n{prefix.strip()} ")
            return "break"
        if any(op in current_line_stripped for op in "+-*/%") and current_line_stripped.endswith('='):
            result = self._evaluate_expression_string(current_line_stripped)
            if result is not None:
                self._is_updating = True
                self.text_widget.insert(tk.INSERT, f" {result}")
                self._is_updating = False
                return "break"
        return

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_file = "config.json"
        self.app_config = {}
        self._load_config()
        self.lang = UI_STRINGS.get(self.app_config.get("language", "en"), UI_STRINGS["en"])
        self.title(self.lang.get("app_title"))
        
        # Set window icon
        try:
            # The icon file should be in the same directory as the script
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '计算笔记本.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            # Silently fail if icon setting fails, it's not a critical error
            pass
            
        self.geometry("800x600")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        self._create_menu()
        self.new_tab()
    def _load_config(self):
        default_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        default_font = ("Arial", 14)
        default_config = {"default_save_directory": default_dir, "language": "en", "font": default_font}
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f: self.app_config = json.load(f)
                for key, value in default_config.items(): self.app_config.setdefault(key, value)
            else:
                self.app_config = default_config
                self._save_config()
        except (json.JSONDecodeError, IOError): self.app_config = default_config
    def _save_config(self):
        with open(self.config_file, 'w') as f: json.dump(self.app_config, f, indent=4)
    def _create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.lang["file"], menu=file_menu)
        file_menu.add_command(label=self.lang["new_tab"], command=self.new_tab)
        file_menu.add_command(label=self.lang["open_file"], command=self.open_file)
        file_menu.add_command(label=self.lang["save"], command=self.save_current_tab)
        file_menu.add_command(label=self.lang["save_as"], command=self.save_current_tab_as)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang["close_tab"], command=self.close_current_tab)
        file_menu.add_command(label=self.lang["exit"], command=self.on_close)
        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.lang["format"], menu=format_menu)
        format_menu.add_command(label=self.lang["font"], command=self.change_font)
        format_menu.add_command(label=self.lang["insert_heading"], command=self.insert_numbered_heading)
        format_menu.add_separator()
        format_menu.add_command(label=self.lang["recalculate_all"], command=self.trigger_recalculate_all)
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.lang["settings"], menu=settings_menu)
        settings_menu.add_command(label=self.lang["set_default_dir"], command=self.set_default_directory)
        lang_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=self.lang["language"], menu=lang_menu)
        lang_menu.add_command(label="English", command=lambda: self.set_language("en"))
        lang_menu.add_command(label="中文", command=lambda: self.set_language("zh"))
    def trigger_recalculate_all(self):
        ct = self.get_current_tab()
        if ct: ct.recalculate_all()
    def get_current_tab(self):
        selected_tab_id = self.notebook.select()
        return self.notebook.nametowidget(selected_tab_id) if selected_tab_id else None
    def new_tab(self, file_path=None):
        font_tuple = tuple(self.app_config.get("font", ("Arial", 14)))
        frame = CalculatorTab(self.notebook, file_path=file_path, current_font=font_tuple)
        title = os.path.basename(file_path) if file_path else "Untitled"
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)
    def open_file(self):
        fp = filedialog.askopenfilename(initialdir=self.app_config["default_save_directory"])
        if fp: self.new_tab(file_path=fp)
    def save_current_tab(self):
        ct = self.get_current_tab()
        if not ct: return
        if ct.file_path:
            try:
                with open(ct.file_path, "w", encoding="utf-8") as f: f.write(ct.text_widget.get("1.0", tk.END))
                ct.has_unsaved_changes = False
            except Exception as e: messagebox.showerror("Error", f"Failed to save file: {e}")
        else: self.save_current_tab_as()
    def save_current_tab_as(self):
        ct = self.get_current_tab()
        if not ct: return
        fp = filedialog.asksaveasfilename(initialdir=self.app_config["default_save_directory"])
        if fp:
            ct.file_path = fp
            self.notebook.tab(ct, text=os.path.basename(fp))
            self.save_current_tab()
    def close_current_tab(self):
        ct = self.get_current_tab()
        if not ct: return
        if ct.has_unsaved_changes:
            res = messagebox.askyesnocancel(self.lang["save_changes_prompt"], self.lang["save_changes_message"].format(tab_name=self.notebook.tab(ct, 'text')))
            if res is None: return
            if res: self.save_current_tab()
        self.notebook.forget(ct)
    def on_close(self):
        for tab_id in list(self.notebook.tabs()):
            self.notebook.select(tab_id)
            ct = self.get_current_tab()
            if not ct: continue
            if ct.has_unsaved_changes:
                res = messagebox.askyesnocancel(self.lang["save_changes_prompt"], self.lang["save_changes_message"].format(tab_name=self.notebook.tab(ct, 'text')))
                if res is None: return
                if res: self.save_current_tab()
        self.save_snapshot_on_close()
        self.destroy()
    def save_snapshot_on_close(self):
        if not self.notebook.tabs(): return
        all_content, now = [], datetime.datetime.now()
        for tab_id in self.notebook.tabs():
            widget, title = self.notebook.nametowidget(tab_id), self.notebook.tab(tab_id, "text")
            all_content.extend([f"\n{'='*40}\n== Tab: {title}\n{'='*40}\n", widget.text_widget.get("1.0", tk.END)])
        base_fn, i = now.strftime("%Y-%m-%d_%H-%M-%S"), 1
        fp = f"{base_fn}.txt"
        while os.path.exists(fp):
            fp = f"{base_fn} ({i}).txt"; i += 1
        try:
            with open(fp, "w", encoding="utf-8") as f: f.write("".join(all_content))
        except Exception as e: messagebox.showerror("Snapshot Error", f"Failed to save session snapshot: {e}")
    def insert_numbered_heading(self):
        ct = self.get_current_tab()
        if not ct: return
        text_widget, all_text = ct.text_widget, ct.text_widget.get("1.0", tk.END)
        headings = re.findall(r"^(\d+)\\.", all_text, re.MULTILINE)
        new_num = max(map(int, headings)) + 1 if headings else 1
        text_widget.insert(tk.INSERT, f"\n{new_num}. ")
    def change_font(self):
        ct = self.get_current_tab()
        if not ct: return
        dialog = FontDialog(self, ct.current_font)
        self.wait_window(dialog)
        if dialog.result:
            new_font, self.app_config["font"] = dialog.result, list(dialog.result)
            ct.text_widget.config(font=new_font)
            ct.current_font = new_font
            self._save_config()
    def set_language(self, lang_code):
        self.app_config["language"] = lang_code
        self._save_config()
        messagebox.showinfo(UI_STRINGS[lang_code]["restart_required_title"], UI_STRINGS[lang_code]["restart_required_message"])
    def set_default_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.app_config.get("default_save_directory"))
        if new_dir:
            self.app_config["default_save_directory"] = new_dir
            self._save_config()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()