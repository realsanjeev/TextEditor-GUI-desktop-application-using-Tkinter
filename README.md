# 📝 Real Text Editor

A modern, feature-rich Notepad clone built with Python and Tkinter, featuring a sleek dark theme and professional UI/UX.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### Modern UI/UX
- **Dark Theme**: Professional dark color scheme with carefully selected colors for optimal readability
- **Line Numbers**: Real-time line number display that scrolls with your content
- **Icon Toolbar**: Quick access to common operations with emoji icons
- **Enhanced Status Bar**: Shows current file, line/column position, total lines, word count, and character count
- **Responsive Design**: Smooth resizing and adaptive layout
- **Zoom Controls**: Easily adjust text size with Ctrl+Plus/Minus/0
- **Cross-Platform Fonts**: Optimized font selection for Windows, macOS, and Linux

### Text Editing
- **Find & Replace**: Modern dialog with syntax highlighting for search results
- **Undo/Redo**: Full undo/redo support for all editing operations
- **Standard Operations**: Cut, copy, paste, select all functionality
- **Word Wrap**: Automatic word wrapping for better readability

### File Operations
- **Multiple File Types**: Support for .txt, .py, and all file types
- **Auto-Save Prompts**: Never lose your work with exit confirmation
- **UTF-8 Encoding**: Proper encoding support for international characters

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select All |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl++` | Zoom In |
| `Ctrl+-` | Zoom Out |
| `Ctrl+0` | Reset Zoom |

## 🚀 Quick Start

### Prerequisites

> 💡 **Linux users:**  
> You might need to install `tkinter`:  
> ```bash  
> sudo apt-get install python3-tk  
> ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/realsanjeev/Notepad-Clone-in-Python.git
   cd Notepad-Clone-in-Python
   ```

2. **Create a virtual environment** 🐍  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application** ▶️  
   ```bash
   python3 main.py
   ```

## 🎨 Design Philosophy

This text editor combines functionality with aesthetics, featuring:
- **Color Scheme**: Carefully selected dark theme colors for reduced eye strain
- **Typography**: Monospace fonts (Consolas, Monaco) for better code readability
- **Spacing**: Generous padding and margins for a comfortable editing experience
- **Visual Feedback**: Hover effects and selection highlighting for better UX

## 🏗️ Architecture

```
Notepad-Clone-in-Python/
├── main.py              # Main application with UI components
├── src/
│   └── view.py         # About dialog and helper views
├── images/
│   ├── computer.ico    # Application icon
│   └── search.ico      # Search icon
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Key Components

- **LineNumbers**: Custom Canvas widget for displaying line numbers
- **Toolbar**: Frame with icon buttons for quick actions
- **RealMenu**: Menu bar with File, Edit, View, and Help menus
- **Text Editor**: Customized Text widget with modern styling

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Tkinter**: GUI framework (built-in with Python)
- **Pillow (PIL)**: Image processing for icons
- **ttk**: Themed widgets for modern look

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add syntax highlighting for different programming languages
- Implement tabs for multiple file editing
- Add themes (light mode, custom color schemes)
- Create a settings/preferences dialog
- Add recent files menu
- Implement auto-save functionality

## 📝 License

This project is open source and available for educational purposes.

## 📧 Contact

**Developer**: [@realsanjeev](https://github.com/realsanjeev)

<table>
  <tr>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/instagram.png" alt="Instagram" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/twitter.png" alt="Twitter" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/github.png" alt="GitHub" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/linkedin-logo.png" alt="LinkedIn" width="50" height="50"></td>
  </tr>
</table>

## 🙏 Acknowledgments

- Inspired by classic Notepad and modern code editors
- Built with guidance from:
  - [Creating GUI with Tkinter](https://www.pythonguis.com/tutorials/create-gui-tkinter/)
  - [Tkinter Python Documentation](https://docs.python.org/3/library/tk.html)
  - [TkDocs](https://tkdocs.com/pyref/frame.html)

---

<div align="center">
Made with ❤️ by @realsanjeev
</div>
