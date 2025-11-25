import os
import sys
from tkinter import (Tk, Menu, Frame, Button, Toplevel, Canvas,
                     Label, Text, Entry, ttk,
                     filedialog as fd)
from tkinter.messagebox import askquestion, showinfo
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk

from src.view import getAboutEditor, show_welcome_tips, show_quick_reference

# Modern color scheme
COLORS = {
    'bg': '#1e1e1e',           # Main background
    'editor_bg': '#2d2d2d',    # Text editor background
    'editor_fg': '#d4d4d4',    # Text color
    'accent': '#007acc',        # Accent blue
    'menu_bg': '#252526',       # Menu background
    'status_bg': '#007acc',     # Status bar background
    'status_fg': '#ffffff',     # Status bar text
    'line_num_bg': '#1e1e1e',   # Line numbers background
    'line_num_fg': '#858585',   # Line numbers text
    'selection': '#264f78',     # Selection color
    'button_hover': '#094771',  # Button hover
}

root = Tk()
root.wm_title('Real Text Editor')
root.configure(background=COLORS['bg'])

# Icon of the app (with error handling)
try:
    im = Image.open('images/computer.ico')
    photo = ImageTk.PhotoImage(im)
    root.wm_iconphoto(True, photo)
except Exception as e:
    print(f"Warning: Could not load icon: {e}")

# set a minimum window size (width, height)
root.minsize(800, 600)
root.geometry('1200x800')

# Global variables
FILE = None
CURRENT_FONT_SIZE = 11

# Cross-platform font selection
if sys.platform == 'win32':
    EDITOR_FONT = ('Consolas', CURRENT_FONT_SIZE)
elif sys.platform == 'darwin':
    EDITOR_FONT = ('Monaco', CURRENT_FONT_SIZE)
else:
    EDITOR_FONT = ('DejaVu Sans Mono', CURRENT_FONT_SIZE)


class LineNumbers(Canvas):
    """Canvas widget to display line numbers for the text editor."""
    
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.text_widget = text_widget
        self.config(
            width=50,
            bg=COLORS['line_num_bg'],
            highlightthickness=0,
            bd=0
        )
        
    def redraw(self, *args):
        """Redraw line numbers."""
        self.delete("all")
        
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2, y,
                anchor="nw",
                text=linenum,
                fill=COLORS['line_num_fg'],
                font=("Consolas", 10)
            )
            i = self.text_widget.index(f"{i}+1line")


class Toolbar(Frame):
    """Toolbar with icon buttons for common operations."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg=COLORS['menu_bg'], pady=5, padx=5)
        
        # Define toolbar buttons
        buttons = [
            ('New', get_new_file, '📄'),
            ('Open', get_open_file, '📂'),
            ('Save', get_save_file, '💾'),
            ('|', None, '|'),  # Separator
            ('Cut', get_cut, '✂️'),
            ('Copy', get_copy, '📋'),
            ('Paste', get_paste, '📌'),
            ('|', None, '|'),  # Separator
            ('Undo', get_undo_edit, '↶'),
            ('Redo', get_redo_edit, '↷'),
        ]
        
        for label, command, icon in buttons:
            if label == '|':
                # Separator
                sep = Frame(self, width=2, bg=COLORS['line_num_fg'])
                sep.pack(side='left', fill='y', padx=5)
            else:
                btn = Button(
                    self,
                    text=f"{icon} {label}",
                    command=command,
                    bg=COLORS['menu_bg'],
                    fg=COLORS['editor_fg'],
                    activebackground=COLORS['button_hover'],
                    activeforeground=COLORS['status_fg'],
                    relief='flat',
                    padx=10,
                    pady=5,
                    cursor='hand2',
                    font=('Segoe UI', 9)
                )
                btn.pack(side='left', padx=2)
                
                # Hover effects
                def on_enter(e, b=btn):
                    b.config(bg=COLORS['button_hover'])
                
                def on_leave(e, b=btn):
                    b.config(bg=COLORS['menu_bg'])
                
                btn.bind('<Enter>', on_enter)
                btn.bind('<Leave>', on_leave)


class RealMenu(Menu):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=COLORS['menu_bg'], fg=COLORS['editor_fg'])
        
        file_menu = Menu(self, tearoff=0, bg=COLORS['menu_bg'], fg=COLORS['editor_fg'])
        file_menu.add_command(label='New                    Ctrl+N', command=get_new_file)
        file_menu.add_command(label='Open                  Ctrl+O', command=get_open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Save                   Ctrl+S', command=get_save_file)
        file_menu.add_command(label='Save As        Ctrl+Shift+S', command=get_save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit                     Alt+F4', command=get_exit_file)
        self.add_cascade(label='File', menu=file_menu)
        
        edit_menu = Menu(self, tearoff=0, bg=COLORS['menu_bg'], fg=COLORS['editor_fg'])
        edit_menu.add_command(label='Undo                  Ctrl+Z', command=get_undo_edit)
        edit_menu.add_command(label='Redo                   Ctrl+Y', command=get_redo_edit)
        edit_menu.add_separator()
        edit_menu.add_command(label='Cut                     Ctrl+X', command=get_cut)
        edit_menu.add_command(label='Copy                  Ctrl+C', command=get_copy)
        edit_menu.add_command(label='Paste                  Ctrl+V', command=get_paste)
        edit_menu.add_command(label='Select All            Ctrl+A', command=get_select_all)
        edit_menu.add_separator()
        edit_menu.add_command(label='Find                    Ctrl+F', command=self.get_find_edit)
        edit_menu.add_command(label='Replace              Ctrl+H', command=self.get_find_edit)
        self.add_cascade(label='Edit', menu=edit_menu)
        
        view_menu = Menu(self, tearoff=0, bg=COLORS['menu_bg'], fg=COLORS['editor_fg'])
        view_menu.add_command(label='Zoom In              Ctrl++', command=zoom_in)
        view_menu.add_command(label='Zoom Out           Ctrl+-', command=zoom_out)
        view_menu.add_command(label='Reset Zoom         Ctrl+0', command=zoom_reset)
        view_menu.add_separator()
        view_menu.add_command(label='Toggle Status Bar', command=toggle_status_bar)
        self.add_cascade(label='View', menu=view_menu)
        
        help_menu = Menu(self, tearoff=0, bg=COLORS['menu_bg'], fg=COLORS['editor_fg'])
        help_menu.add_command(label='Welcome Tips', command=lambda: show_welcome_tips(root))
        help_menu.add_command(label='Keyboard Shortcuts', command=lambda: show_quick_reference(root))
        help_menu.add_separator()
        help_menu.add_command(label='About', command=lambda: getAboutEditor(root))
        self.add_cascade(label='Help', menu=help_menu)
        
        master.config(menu=self)

    def get_find_edit(self):
        """Open find and replace dialog with modern styling."""
        child_window = Toplevel(self)
        child_window.title("Find and Replace")
        child_window.configure(bg=COLORS['bg'])
        child_window.geometry('450x150')
        child_window.resizable(False, False)
        
        # Configure grid weights
        child_window.grid_columnconfigure(1, weight=1)
        
        # Find section
        Label(
            child_window,
            text='Find:',
            bg=COLORS['bg'],
            fg=COLORS['editor_fg'],
            font=('Segoe UI', 10)
        ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        find_entry = Entry(
            child_window,
            bg=COLORS['editor_bg'],
            fg=COLORS['editor_fg'],
            insertbackground=COLORS['editor_fg'],
            font=('Consolas', 10)
        )
        find_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        find_btn = Button(
            child_window,
            text='Find',
            command=lambda: find(find_entry),
            bg=COLORS['accent'],
            fg=COLORS['status_fg'],
            activebackground=COLORS['button_hover'],
            relief='flat',
            padx=15,
            cursor='hand2',
            font=('Segoe UI', 9)
        )
        find_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Replace section
        Label(
            child_window,
            text='Replace:',
            bg=COLORS['bg'],
            fg=COLORS['editor_fg'],
            font=('Segoe UI', 10)
        ).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        replace_entry = Entry(
            child_window,
            bg=COLORS['editor_bg'],
            fg=COLORS['editor_fg'],
            insertbackground=COLORS['editor_fg'],
            font=('Consolas', 10)
        )
        replace_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        replace_btn = Button(
            child_window,
            text='Replace All',
            command=lambda: find_and_replace(find_entry, replace_entry),
            bg=COLORS['accent'],
            fg=COLORS['status_fg'],
            activebackground=COLORS['button_hover'],
            relief='flat',
            padx=15,
            cursor='hand2',
            font=('Segoe UI', 9)
        )
        replace_btn.grid(row=1, column=2, padx=10, pady=10)
        
        find_entry.focus()


def find(edit):
    """Find text in the editor and highlight matches."""
    text_editor.tag_remove('found', '1.0', 'end')
    search = edit.get()
    if search:
        idx = '1.0'
        while True:
            idx = text_editor.search(search, idx, nocase=1, stopindex='end')
            if not idx:
                break
            lastidx = f'{idx} + {len(search)}c'
            text_editor.tag_add('found', idx, lastidx)
            idx = lastidx
        text_editor.tag_config('found', background=COLORS['accent'], foreground=COLORS['status_fg'])


def find_and_replace(edit, edit2):
    """Replace all occurrences of search text with replacement text."""
    search, replace = edit.get(), edit2.get()
    if search and replace:
        text_content = text_editor.get('1.0', 'end-1c')
        new_content = text_content.replace(search, replace)
        text_editor.delete('1.0', 'end')
        text_editor.insert('1.0', new_content)
        showinfo('Replace', f'Replaced all occurrences of "{search}" with "{replace}"')


def get_new_file():
    """Create a new file."""
    global FILE
    FILE = None
    root.title("Untitled - Real Text Editor")
    text_editor.delete(1.0, 'end')


def get_open_file():
    """Open an existing file."""
    global FILE
    file_path = fd.askopenfilename(filetypes=[('Text Files', '*.txt'), ('Python Files', '*.py'), ('All Files', '*.*')])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_editor.delete(1.0, 'end')
                text_editor.insert('1.0', file.read())
            FILE = file_path  # Fix: Update FILE variable
            root.title(f'{os.path.basename(file_path)} - Real Text Editor')
        except Exception as e:
            showinfo('Error', f'Could not open file: {str(e)}')


def get_save_as_file():
    """Save file with a new name."""
    global FILE
    file_path = asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text Files', '*.txt'), ('Python Files', '*.py'), ('All Files', '*.*')]
    )
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_editor.get('1.0', 'end-1c'))
            FILE = file_path
            root.title(f'{os.path.basename(file_path)} - Real Text Editor')
            showinfo('Success', 'File saved successfully!')
        except Exception as e:
            showinfo('Error', f'Could not save file: {str(e)}')


def get_save_file():
    """Save the current file."""
    global FILE
    if FILE:
        try:
            with open(FILE, 'w', encoding='utf-8') as file:
                file.write(text_editor.get('1.0', 'end-1c'))
            showinfo('Success', 'File saved successfully!')
        except Exception as e:
            showinfo('Error', f'Could not save file: {str(e)}')
    else:
        get_save_as_file()


def get_exit_file():
    """Exit the application."""
    if askquestion('Exit', 'Do you want to save changes before quitting?') == 'yes':
        get_save_file()
    root.quit()


def update_status(event=None):
    """Update the status bar with current line, column, total lines, and word count."""
    if status_bar.winfo_ismapped():
        total_lines = int(text_editor.index('end-1c').split('.')[0])
        line, col = text_editor.index('insert').split('.')
        
        # Get word count
        content = text_editor.get('1.0', 'end-1c')
        word_count = len(content.split()) if content.strip() else 0
        char_count = len(content)
        
        # Update filename if available
        filename_display = os.path.basename(FILE) if FILE else "Untitled"
        
        # Update the status bar
        status_label.config(
            text=f"  {filename_display}  |  Ln {line}, Col {col}  |  Lines: {total_lines}  |  Words: {word_count}  |  Chars: {char_count}  "
        )
    
    # Update line numbers
    line_numbers.redraw()


def toggle_status_bar():
    """Toggle the visibility of the status bar."""
    if status_bar.winfo_ismapped():
        status_bar.grid_remove()
    else:
        status_bar.grid()


def show_shortcuts():
    """Display keyboard shortcuts using the modern dialog."""
    show_quick_reference(root)


def get_undo_edit():
    """Undo the last edit."""
    try:
        text_editor.edit_undo()
    except:
        pass


def get_redo_edit():
    """Redo the last undone edit."""
    try:
        text_editor.edit_redo()
    except:
        pass


def get_copy():
    """Copy selected text."""
    text_editor.event_generate("<<Copy>>")


def get_cut():
    """Cut selected text."""
    text_editor.event_generate("<<Cut>>")


def get_paste():
    """Paste text from clipboard."""
    text_editor.event_generate("<<Paste>>")


def get_select_all():
    """Select all text."""
    text_editor.tag_add('sel', '1.0', 'end')
    return 'break'


def zoom_in():
    """Increase font size."""
    global CURRENT_FONT_SIZE, EDITOR_FONT
    CURRENT_FONT_SIZE = min(CURRENT_FONT_SIZE + 2, 32)  # Max size 32
    if sys.platform == 'win32':
        EDITOR_FONT = ('Consolas', CURRENT_FONT_SIZE)
    elif sys.platform == 'darwin':
        EDITOR_FONT = ('Monaco', CURRENT_FONT_SIZE)
    else:
        EDITOR_FONT = ('DejaVu Sans Mono', CURRENT_FONT_SIZE)
    text_editor.config(font=EDITOR_FONT)


def zoom_out():
    """Decrease font size."""
    global CURRENT_FONT_SIZE, EDITOR_FONT
    CURRENT_FONT_SIZE = max(CURRENT_FONT_SIZE - 2, 8)  # Min size 8
    if sys.platform == 'win32':
        EDITOR_FONT = ('Consolas', CURRENT_FONT_SIZE)
    elif sys.platform == 'darwin':
        EDITOR_FONT = ('Monaco', CURRENT_FONT_SIZE)
    else:
        EDITOR_FONT = ('DejaVu Sans Mono', CURRENT_FONT_SIZE)
    text_editor.config(font=EDITOR_FONT)


def zoom_reset():
    """Reset font size to default."""
    global CURRENT_FONT_SIZE, EDITOR_FONT
    CURRENT_FONT_SIZE = 11
    if sys.platform == 'win32':
        EDITOR_FONT = ('Consolas', CURRENT_FONT_SIZE)
    elif sys.platform == 'darwin':
        EDITOR_FONT = ('Monaco', CURRENT_FONT_SIZE)
    else:
        EDITOR_FONT = ('DejaVu Sans Mono', CURRENT_FONT_SIZE)
    text_editor.config(font=EDITOR_FONT)


# Create main container
main_container = Frame(root, bg=COLORS['bg'])
main_container.grid(row=1, column=0, sticky='nsew')

# Create toolbar
toolbar = Toolbar(main_container)
toolbar.grid(row=0, column=0, columnspan=3, sticky='ew')

# Create text editor with custom font and colors
text_editor = Text(
    main_container,
    wrap='word',
    undo=True,
    bg=COLORS['editor_bg'],
    fg=COLORS['editor_fg'],
    insertbackground=COLORS['editor_fg'],
    selectbackground=COLORS['selection'],
    selectforeground=COLORS['status_fg'],
    font=EDITOR_FONT,
    relief='flat',
    padx=10,
    pady=10
)

# Create line numbers
line_numbers = LineNumbers(main_container, text_editor)
line_numbers.grid(row=1, column=0, sticky='ns')

# Create scrollbar
scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=text_editor.yview)
text_editor.config(yscrollcommand=scrollbar.set)

# Grid layout
text_editor.grid(row=1, column=1, sticky='nsew')
scrollbar.grid(row=1, column=2, sticky='ns')

# Create status bar
status_bar = Frame(root, bg=COLORS['status_bg'], height=25)
status_label = Label(
    status_bar,
    text="  Ready  ",
    bg=COLORS['status_bg'],
    fg=COLORS['status_fg'],
    font=('Segoe UI', 9),
    anchor='w'
)
status_label.pack(fill='both', expand=True)
status_bar.grid(row=2, column=0, sticky='ew')

# Configure root window grid to allow resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure main container grid
main_container.grid_rowconfigure(1, weight=1)
main_container.grid_columnconfigure(1, weight=1)

# Bind events for status updates and line numbers
text_editor.bind('<KeyRelease>', update_status)
text_editor.bind('<ButtonRelease>', update_status)
text_editor.bind('<MouseWheel>', lambda e: line_numbers.redraw())
text_editor.bind('<Configure>', lambda e: line_numbers.redraw())

# Bind keyboard shortcuts
root.bind("<Control-n>", lambda e: get_new_file())
root.bind("<Control-N>", lambda e: get_new_file())
root.bind("<Control-o>", lambda e: get_open_file())
root.bind("<Control-O>", lambda e: get_open_file())
root.bind("<Control-s>", lambda e: get_save_file())
root.bind("<Control-S>", lambda e: get_save_file())
root.bind("<Control-Shift-s>", lambda e: get_save_as_file())
root.bind("<Control-Shift-S>", lambda e: get_save_as_file())
root.bind("<Control-a>", lambda e: get_select_all())
root.bind("<Control-A>", lambda e: get_select_all())
root.bind("<Control-f>", lambda e: RealMenu(root).get_find_edit())
root.bind("<Control-F>", lambda e: RealMenu(root).get_find_edit())
root.bind("<Control-h>", lambda e: RealMenu(root).get_find_edit())
root.bind("<Control-H>", lambda e: RealMenu(root).get_find_edit())

# Zoom shortcuts
root.bind("<Control-plus>", lambda e: zoom_in())
root.bind("<Control-equal>", lambda e: zoom_in())  # For keyboards without numpad
root.bind("<Control-minus>", lambda e: zoom_out())
root.bind("<Control-0>", lambda e: zoom_reset())

# Create menu
main_menu = RealMenu(root)

# Initial status update
update_status()

if __name__ == '__main__':
    root.mainloop()
