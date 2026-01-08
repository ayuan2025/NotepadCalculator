# Notepad Calculator v1.0.0

A simple-to-use, powerful, and elegant notepad with built-in calculation capabilities. This application blends the simplicity of a text editor with the power of a calculator, allowing you to perform calculations inline with your notes.

## Features

- **Inline Calculation**: Write calculations naturally within your text (e.g., `The total cost is 100 * 15% = 15`). The app will automatically update the result if you change the expression.
- **Explicit Calculation**: Trigger a calculation by ending a line with an equals sign (e.g., `(1920 / 16) * 9 =`) and pressing Enter.
- **Multi-Tab Interface**: Work on multiple documents at once with a clean, tabbed interface.
- **Automatic Lists**: Create numbered (`1.`) or bulleted (`*`, `-`) lists that automatically continue when you press Enter.
- **Persistent Sessions**: Your open tabs and their content are saved on exit and restored when you reopen the app (via a timestamped snapshot file).
- **Customization**:
  - **Multi-Language**: Switch between English and Chinese for the UI.
  - **Font Settings**: Choose your preferred font and font size.
  - **Default Directory**: Set your own default folder for opening and saving files.
- **File Support**: Full support for opening, saving, and creating `.txt` files.
- **Notion Export**: Export your notes and calculations to a Notion database.

## How to Use

1.  **Calculations**:
    - For a new calculation, type an expression like `(100 + 50) * 2 =` and press **Enter**.
    - To update an existing calculation, simply change the numbers in the expression. The result will update automatically as you type.
2.  **Lists**:
    - Start a line with `1.` or `*` followed by a space.
    - Press **Enter** to automatically create the next item in the list.
    - Press **Enter** on an empty list item to exit the list.
3.  **Pasting**:
    - Paste text containing expressions, then use **Format > Recalculate All** to update all calculations at once.
