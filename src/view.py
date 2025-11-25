import textwrap
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Toplevel, Label, Button, Frame, Text, Scrollbar


# Modern color scheme (matching main.py)
COLORS = {
    'bg': '#1e1e1e',
    'editor_bg': '#2d2d2d',
    'editor_fg': '#d4d4d4',
    'accent': '#007acc',
    'menu_bg': '#252526',
    'status_bg': '#007acc',
    'status_fg': '#ffffff',
    'button_hover': '#094771',
}


def create_modern_dialog(parent, title, width=500, height=400):
    """
    Create a modern-styled dialog window.
    
    Args:
        parent: Parent window
        title: Dialog title
        width: Window width
        height: Window height
    
    Returns:
        Toplevel window with modern styling
    """
    dialog = Toplevel(parent)
    dialog.title(title)
    dialog.geometry(f'{width}x{height}')
    dialog.configure(bg=COLORS['bg'])
    dialog.resizable(False, False)
    
    # Center the dialog on screen
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    return dialog


def create_styled_button(parent, text, command, **kwargs):
    """
    Create a modern-styled button.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Button command
        **kwargs: Additional button options
    
    Returns:
        Styled Button widget
    """
    btn = Button(
        parent,
        text=text,
        command=command,
        bg=COLORS['accent'],
        fg=COLORS['status_fg'],
        activebackground=COLORS['button_hover'],
        activeforeground=COLORS['status_fg'],
        relief='flat',
        padx=20,
        pady=8,
        cursor='hand2',
        font=('Segoe UI', 10, 'bold'),
        **kwargs
    )
    
    # Hover effects
    def on_enter(e):
        btn.config(bg=COLORS['button_hover'])
    
    def on_leave(e):
        btn.config(bg=COLORS['accent'])
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    return btn


def getAboutEditor(parent=None):
    """
    Display a modern About dialog with information about Real Text Editor.
    
    Args:
        parent: Parent window (optional)
    
    Returns:
        None
    """
    dialog = create_modern_dialog(parent, 'About Real Text Editor', 550, 500)
    
    # Header with title
    header_frame = Frame(dialog, bg=COLORS['accent'], height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    title_label = Label(
        header_frame,
        text='Real Text Editor',
        font=('Segoe UI', 24, 'bold'),
        bg=COLORS['accent'],
        fg=COLORS['status_fg']
    )
    title_label.pack(pady=20)
    
    version_label = Label(
        header_frame,
        text='Version 2.0',
        font=('Segoe UI', 10),
        bg=COLORS['accent'],
        fg=COLORS['status_fg']
    )
    version_label.pack()
    
    # Content area
    content_frame = Frame(dialog, bg=COLORS['bg'])
    content_frame.pack(fill='both', expand=True, padx=30, pady=20)
    
    # Description
    desc_label = Label(
        content_frame,
        text='A modern, feature-rich text editor built with Python and Tkinter.',
        font=('Segoe UI', 11),
        bg=COLORS['bg'],
        fg=COLORS['editor_fg'],
        wraplength=450,
        justify='center'
    )
    desc_label.pack(pady=(0, 20))
    
    # Features section
    features_title = Label(
        content_frame,
        text='✨ Key Features',
        font=('Segoe UI', 12, 'bold'),
        bg=COLORS['bg'],
        fg=COLORS['accent']
    )
    features_title.pack(anchor='w', pady=(10, 5))
    
    features = [
        '• Modern dark theme interface',
        '• Line numbers display',
        '• Syntax highlighting for search results',
        '• Toolbar with quick access buttons',
        '• Zoom controls (Ctrl+Plus/Minus/0)',
        '• Word and character count',
        '• Comprehensive keyboard shortcuts',
        '• Find and replace functionality',
        '• Cross-platform font support'
    ]
    
    for feature in features:
        feature_label = Label(
            content_frame,
            text=feature,
            font=('Segoe UI', 10),
            bg=COLORS['bg'],
            fg=COLORS['editor_fg'],
            anchor='w'
        )
        feature_label.pack(anchor='w', pady=2)
    
    # Developer info
    dev_frame = Frame(content_frame, bg=COLORS['editor_bg'], relief='flat')
    dev_frame.pack(fill='x', pady=(20, 10))
    
    dev_label = Label(
        dev_frame,
        text='👨‍💻 Developed by: @realsanjeev',
        font=('Segoe UI', 10),
        bg=COLORS['editor_bg'],
        fg=COLORS['editor_fg']
    )
    dev_label.pack(pady=10)
    
    tech_label = Label(
        dev_frame,
        text='Built with Python, Tkinter, and Pillow',
        font=('Segoe UI', 9),
        bg=COLORS['editor_bg'],
        fg=COLORS['editor_fg']
    )
    tech_label.pack(pady=(0, 5))
    
    purpose_label = Label(
        dev_frame,
        text='Developed for educational purposes',
        font=('Segoe UI', 9, 'italic'),
        bg=COLORS['editor_bg'],
        fg=COLORS['editor_fg']
    )
    purpose_label.pack(pady=(0, 10))
    
    # Copyright
    copyright_label = Label(
        content_frame,
        text='© 2025 Real Text Editor',
        font=('Segoe UI', 9),
        bg=COLORS['bg'],
        fg=COLORS['editor_fg']
    )
    copyright_label.pack(pady=(10, 0))
    
    # Close button
    button_frame = Frame(dialog, bg=COLORS['bg'])
    button_frame.pack(fill='x', padx=30, pady=(0, 20))
    
    close_btn = create_styled_button(button_frame, 'Close', dialog.destroy)
    close_btn.pack()
    
    # Make dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    if parent:
        parent.wait_window(dialog)


def show_welcome_tips(parent=None):
    """
    Display a welcome dialog with quick tips for new users.
    
    Args:
        parent: Parent window (optional)
    
    Returns:
        None
    """
    dialog = create_modern_dialog(parent, 'Welcome to Real Text Editor', 600, 450)
    
    # Header
    header_frame = Frame(dialog, bg=COLORS['accent'], height=70)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    title_label = Label(
        header_frame,
        text='🎉 Welcome to Real Text Editor!',
        font=('Segoe UI', 18, 'bold'),
        bg=COLORS['accent'],
        fg=COLORS['status_fg']
    )
    title_label.pack(pady=20)
    
    # Content
    content_frame = Frame(dialog, bg=COLORS['bg'])
    content_frame.pack(fill='both', expand=True, padx=30, pady=20)
    
    intro_label = Label(
        content_frame,
        text='Get started with these quick tips:',
        font=('Segoe UI', 11),
        bg=COLORS['bg'],
        fg=COLORS['editor_fg']
    )
    intro_label.pack(anchor='w', pady=(0, 15))
    
    tips = [
        ('📄 File Operations', 'Use Ctrl+N for new file, Ctrl+O to open, Ctrl+S to save'),
        ('✂️ Editing', 'Standard shortcuts: Ctrl+X/C/V for cut/copy/paste, Ctrl+Z/Y for undo/redo'),
        ('🔍 Find & Replace', 'Press Ctrl+F to find text, Ctrl+H to replace'),
        ('🔎 Zoom', 'Ctrl++ to zoom in, Ctrl+- to zoom out, Ctrl+0 to reset'),
        ('📊 Status Bar', 'View line/column position, word count, and character count at the bottom'),
        ('⌨️ Shortcuts', 'Check Help → Keyboard Shortcuts for the complete list'),
    ]
    
    for title, description in tips:
        tip_frame = Frame(content_frame, bg=COLORS['editor_bg'])
        tip_frame.pack(fill='x', pady=5)
        
        tip_title = Label(
            tip_frame,
            text=title,
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['editor_bg'],
            fg=COLORS['accent'],
            anchor='w'
        )
        tip_title.pack(anchor='w', padx=10, pady=(8, 2))
        
        tip_desc = Label(
            tip_frame,
            text=description,
            font=('Segoe UI', 9),
            bg=COLORS['editor_bg'],
            fg=COLORS['editor_fg'],
            anchor='w',
            wraplength=520,
            justify='left'
        )
        tip_desc.pack(anchor='w', padx=10, pady=(0, 8))
    
    # Button frame
    button_frame = Frame(dialog, bg=COLORS['bg'])
    button_frame.pack(fill='x', padx=30, pady=(0, 20))
    
    got_it_btn = create_styled_button(button_frame, 'Got it!', dialog.destroy)
    got_it_btn.pack()
    
    # Make dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    if parent:
        parent.wait_window(dialog)


def show_quick_reference(parent=None):
    """
    Display a quick reference card with all keyboard shortcuts.
    
    Args:
        parent: Parent window (optional)
    
    Returns:
        None
    """
    dialog = create_modern_dialog(parent, 'Keyboard Shortcuts Reference', 700, 550)
    
    # Header
    header_frame = Frame(dialog, bg=COLORS['accent'], height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    title_label = Label(
        header_frame,
        text='⌨️ Keyboard Shortcuts',
        font=('Segoe UI', 18, 'bold'),
        bg=COLORS['accent'],
        fg=COLORS['status_fg']
    )
    title_label.pack(pady=15)
    
    # Scrollable content
    content_frame = Frame(dialog, bg=COLORS['bg'])
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Create text widget with scrollbar
    text_widget = Text(
        content_frame,
        bg=COLORS['editor_bg'],
        fg=COLORS['editor_fg'],
        font=('Consolas', 10),
        relief='flat',
        padx=15,
        pady=15,
        wrap='word'
    )
    
    scrollbar = Scrollbar(content_frame, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Shortcuts content
    shortcuts_content = """
FILE OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ctrl+N                    Create a new file
  Ctrl+O                    Open an existing file
  Ctrl+S                    Save current file
  Ctrl+Shift+S              Save file with new name
  Alt+F4                    Exit application

EDITING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ctrl+Z                    Undo last action
  Ctrl+Y                    Redo last undone action
  Ctrl+X                    Cut selected text
  Ctrl+C                    Copy selected text
  Ctrl+V                    Paste from clipboard
  Ctrl+A                    Select all text

SEARCH & REPLACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ctrl+F                    Find text
  Ctrl+H                    Find and replace text

VIEW CONTROLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ctrl++                    Zoom in (increase font size)
  Ctrl+-                    Zoom out (decrease font size)
  Ctrl+0                    Reset zoom to default

TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Line numbers automatically scroll with your text
  • Status bar shows: filename, position, lines, words, and characters
  • Toolbar provides quick access to common operations
  • Find highlights all matches in blue
  • Dark theme reduces eye strain during long editing sessions
"""
    
    text_widget.insert('1.0', shortcuts_content)
    text_widget.config(state='disabled')  # Make read-only
    
    # Close button
    button_frame = Frame(dialog, bg=COLORS['bg'])
    button_frame.pack(fill='x', padx=30, pady=(0, 20))
    
    close_btn = create_styled_button(button_frame, 'Close', dialog.destroy)
    close_btn.pack()
    
    # Make dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    if parent:
        parent.wait_window(dialog)
