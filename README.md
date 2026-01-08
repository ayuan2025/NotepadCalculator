# Notepad Calculator v1.0.0

A simple-to-use, powerful, and elegant notepad with built-in calculation capabilities. This application blends the simplicity of a text editor with the power of a calculator, allowing you to perform calculations inline with your notes.

---

一个简单易用、功能强大且界面优雅的笔记本，内置了计算功能。本应用将文本编辑器的简洁性与计算器的强大功能融为一体，让您可以在笔记中进行内联计算。

---

## Features / 功能

- **Inline Calculation / 内联计算**: Write calculations naturally within your text (e.g., `The total cost is 100 * 15% = 15`). The app will automatically update the result if you change the expression. / 在文本中自然地书写计算式（例如 `总成本为 100 * 15% = 15`）。如果您修改表达式，应用会自动更新结果。

- **Explicit Calculation / 显式计算**: Trigger a calculation by ending a line with an equals sign (e.g., `(1920 / 16) * 9 =`) and pressing Enter. / 在一行的末尾输入等号（例如 `(1920 / 16) * 9 =`）并按回车键来触发计算。

- **Multi-Tab Interface /多标签页界面**: Work on multiple documents at once with a clean, tabbed interface. / 使用简洁的标签页界面同时处理多个文档。

- **Automatic Lists / 自动列表**: Create numbered (`1.`) or bulleted (`*`, `-`) lists that automatically continue when you press Enter. / 创建数字列表（`1.`）或项目符号列表（`*`, `-`），在您按回车时会自动延续。

- **Persistent Sessions / 会话保持**: Your open tabs and their content are saved on exit into a timestamped snapshot file for backup. / 您打开的标签页及其内容在退出时会保存到一个带时间戳的快照文件中进行备份。

- **Customization / 自定义**:
  - **Multi-Language / 多语言**: Switch between English and Chinese for the UI. / 在英文和中文界面之间切换。
  - **Font Settings / 字体设置**: Choose your preferred font and font size. / 选择您偏好的字体和字号。
  - **Default Directory / 默认文件夹**: Set your own default folder for opening and saving files. / 设置您自己的默认文件夹用于打开和保存文件。

- **File Support / 文件支持**: Full support for opening, saving, and creating `.txt` files. / 完全支持打开、保存和创建 `.txt` 文件。

- **Notion Export / 导出到 Notion**: Export your notes and calculations to a Notion database. / 将您的笔记和计算结果导出到 Notion 数据库。

## How to Use / 如何使用

1.  **Calculations / 计算**:
    - For a new calculation, type an expression like `(100 + 50) * 2 =` and press **Enter**. / 对于新计算，输入类似 `(100 + 50) * 2 =` 的表达式，然后按 **回车**。
    - To update an existing calculation, simply change the numbers in the expression. The result will update automatically as you type. / 要更新现有计算，只需更改表达式中的数字即可，结果会在您键入时自动更新。

2.  **Lists / 列表**:
    - Start a line with `1.` or `*` followed by a space. / 以 `1.` 或 `*` 加一个空格来开始一行。
    - Press **Enter** to automatically create the next item in the list. / 按 **回车** 自动创建列表中的下一个项目。
    - Press **Enter** on an empty list item to exit the list. / 在一个空的列表项上按 **回车** 以退出列表。

3.  **Pasting / 粘贴**:
    - Paste text containing expressions, then use **Format > Recalculate All** to update all calculations at once. / 粘贴包含表达式的文本，然后使用 **格式 > 重新计算全部** 来一次性更新所有计算。