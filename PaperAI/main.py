"""PaperAI GUI entry point."""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPalette

from ui.ui import (
    PaperAIApp,
    DARK_BG,
    TEXT_PRIMARY,
    INPUT_BG,
    SIDEBAR_BG,
    BUBBLE_BOT,
    ACCENT,
)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(DARK_BG))
    dark_palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    dark_palette.setColor(QPalette.Base, QColor(INPUT_BG))
    dark_palette.setColor(QPalette.AlternateBase, QColor(SIDEBAR_BG))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(SIDEBAR_BG))
    dark_palette.setColor(QPalette.ToolTipText, QColor(TEXT_PRIMARY))
    dark_palette.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
    dark_palette.setColor(QPalette.Button, QColor(BUBBLE_BOT))
    dark_palette.setColor(QPalette.ButtonText, QColor(TEXT_PRIMARY))
    dark_palette.setColor(QPalette.Highlight, QColor(ACCENT))
    dark_palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(dark_palette)

    window = PaperAIApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()