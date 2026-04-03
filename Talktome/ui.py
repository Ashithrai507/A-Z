import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QFileDialog, QScrollArea,
    QLabel, QHBoxLayout, QFrame, QSizePolicy, QTextEdit, QTextBrowser
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QFontDatabase, QPalette

from main import ask_llm, load_pdf


COLORS = {
    "bg_primary":    "#212121",
    "bg_secondary":  "#2f2f2f",
    "bg_bubble_bot": "#282828",
    "text_primary":  "#ececec",
    "text_secondary":"#9b9b9b",
    "text_dim":      "#5e5e5e",
    "border":        "#383838",
    "input_bg":      "#2c2c2c",
    "send_btn":      "#f0f0f0",
    "send_btn_text": "#1a1a1a",
    "send_hover":    "#d8d8d8",
    "user_bubble":   "#2a2a2a",
    "code_bg":       "#1a1a1a",
    "code_border":   "#3a3a3a",
    "h1_color":      "#ffffff",
    "h2_color":      "#e2e2e2",
    "h3_color":      "#c8c8c8",
    "bullet_color":  "#60a5fa",
    "bold_color":    "#f0f0f0",
    "divider":       "#333333",
    "accent_blue":   "#60a5fa",
}


class ThinkingDots(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 22)
        self._phases = [0.0, 0.33, 0.66]
        self._values = [0.3, 0.3, 0.3]
        self._tick = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.timer.start(55)

    def _step(self):
        import math
        self._tick += 1
        for i in range(3):
            phase = (self._tick / 9.0 + self._phases[i]) % 1.0
            self._values[i] = 0.2 + 0.8 * abs(math.sin(phase * 3.14159))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        dot_r, spacing, y = 4, 15, self.height() // 2
        for i in range(3):
            x = 7 + i * spacing
            alpha = int(self._values[i] * 255)
            painter.setBrush(QBrush(QColor(160, 160, 160, alpha)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x - dot_r, y - dot_r, dot_r * 2, dot_r * 2)

    def stop(self):
        self.timer.stop()


class ThinkingBubble(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        row = QHBoxLayout(self)
        row.setContentsMargins(60, 8, 60, 8)
        row.setSpacing(12)
        row.setAlignment(Qt.AlignLeft)
        avatar = QLabel("\u2736")
        avatar.setFixedSize(30, 30)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; background: transparent;")
        row.addWidget(avatar, alignment=Qt.AlignTop)
        bubble = QFrame()
        bubble.setStyleSheet(f"background-color:{COLORS['bg_bubble_bot']};border-radius:14px;border:1px solid {COLORS['border']};")
        b_layout = QHBoxLayout(bubble)
        b_layout.setContentsMargins(16, 10, 16, 10)
        b_layout.setSpacing(8)
        lbl = QLabel("Thinking")
        lbl.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:13px;font-family:'Segoe UI';")
        b_layout.addWidget(lbl)
        self.dots = ThinkingDots()
        b_layout.addWidget(self.dots)
        row.addWidget(bubble)
        row.addStretch()

    def stop(self):
        self.dots.stop()


def _inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(
        r'`([^`]+)`',
        lambda m: (f'<code style="background:{COLORS["code_bg"]};color:#c9d1d9;' +
                   f'padding:1px 6px;border-radius:4px;font-family:Consolas,monospace;' +
                   f'font-size:13px;border:1px solid {COLORS["code_border"]};">' +
                   f'{m.group(1)}</code>'),
        text
    )
    text = re.sub(
        r'\*\*(.+?)\*\*',
        lambda m: f'<b style="color:{COLORS["bold_color"]};font-weight:700;">{m.group(1)}</b>',
        text
    )
    text = re.sub(
        r'\*(.+?)\*',
        lambda m: f'<i style="color:{COLORS["text_secondary"]};">{m.group(1)}</i>',
        text
    )
    return text


def markdown_to_html(text):
    lines = text.split("\n")
    out = []
    in_code = False
    code_buf = []
    code_lang = ""
    in_ul = False
    in_ol = False

    for line in lines:
        if line.startswith("```"):
            if not in_code:
                if in_ul: out.append("</ul>"); in_ul = False
                if in_ol: out.append("</ol>"); in_ol = False
                in_code = True
                code_lang = line[3:].strip()
                code_buf = []
            else:
                in_code = False
                cc = "\n".join(code_buf).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                lt = (f'<div style="color:{COLORS["text_dim"]};font-size:11px;font-family:Consolas;margin-bottom:8px;">{code_lang}</div>' if code_lang else "")
                out.append(
                    f'<div style="background:{COLORS["code_bg"]};border:1px solid {COLORS["code_border"]};' +
                    f'border-radius:12px;padding:16px 18px;margin:12px 0;">' +
                    lt +
                    f'<pre style="margin:0;padding:0;color:#c9d1d9;font-family:Consolas,Courier,monospace;' +
                    f'font-size:13px;white-space:pre-wrap;word-wrap:break-word;line-height:1.6;">' +
                    cc + "</pre></div>"
                )
                code_buf = []
                code_lang = ""
            continue

        if in_code:
            code_buf.append(line)
            continue

        if line.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<p style="margin:18px 0 6px 0;"><span style="font-size:15px;font-weight:700;color:{COLORS["h3_color"]};">{_inline(line[4:])}</span></p>')
        elif line.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<p style="margin:22px 0 4px 0;"><span style="font-size:17px;font-weight:700;color:{COLORS["h2_color"]};">{_inline(line[3:])}</span></p><hr style="border:none;border-top:1px solid {COLORS["divider"]};margin:4px 0 12px 0;"/>')
        elif line.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<p style="margin:24px 0 10px 0;"><span style="font-size:20px;font-weight:800;color:{COLORS["h1_color"]};">{_inline(line[2:])}</span></p>')
        elif re.match(r"^[-*\u2022]\s+", line):
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul:
                out.append('<ul style="margin:8px 0;padding:0;list-style:none;">')
                in_ul = True
            content = _inline(re.sub(r"^[-*\u2022]\s+", "", line))
            out.append(f'<li style="margin:5px 0 5px 16px;color:{COLORS["text_primary"]};line-height:1.75;"><span style="color:{COLORS["bullet_color"]};margin-right:10px;font-size:15px;">&#x203A;</span>{content}</li>')
        elif re.match(r"^\d+\.\s+", line):
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol:
                out.append(f'<ol style="margin:8px 0;padding-left:24px;color:{COLORS["text_primary"]};">')
                in_ol = True
            content = _inline(re.sub(r"^\d+\.\s+", "", line))
            out.append(f'<li style="margin:5px 0;line-height:1.75;">{content}</li>')
        elif line.strip() in ("---", "***", "___"):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<hr style="border:none;border-top:1px solid {COLORS["divider"]};margin:14px 0;"/>')
        elif line.startswith("> "):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<div style="border-left:3px solid {COLORS["accent_blue"]};padding:8px 14px;margin:10px 0;background:{COLORS["code_bg"]};border-radius:0 8px 8px 0;"><span style="color:{COLORS["text_secondary"]};font-style:italic;">{_inline(line[2:])}</span></div>')
        elif line.strip() == "":
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append('<div style="height:6px;"></div>')
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(f'<p style="margin:3px 0;padding:0;line-height:1.85;color:{COLORS["text_primary"]};">{_inline(line)}</p>')

    if in_ul: out.append("</ul>")
    if in_ol: out.append("</ol>")
    return "\n".join(out)


class BotReplyWidget(QFrame):
    def __init__(self, text=""):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        outer = QHBoxLayout(self)
        outer.setContentsMargins(60, 8, 60, 8)
        outer.setSpacing(14)
        outer.setAlignment(Qt.AlignLeft)

        avatar = QLabel("\u2736")
        avatar.setFixedSize(30, 30)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:13px;background:transparent;")
        outer.addWidget(avatar, alignment=Qt.AlignTop)

        self.card = QFrame()
        self.card.setStyleSheet(f"background-color:{COLORS['bg_bubble_bot']};border-radius:18px;border:1px solid {COLORS['border']};")

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(22, 18, 22, 18)
        card_layout.setSpacing(0)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(False)
        self.browser.setFrameShape(QFrame.NoFrame)
        self.browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.browser.setStyleSheet(
            f"QTextBrowser {{background:transparent;color:{COLORS['text_primary']};border:none;" +
            f"font-size:14px;font-family:'Segoe UI',sans-serif;}}" +
            "QScrollBar {width:0;height:0;}"
        )

        card_layout.addWidget(self.browser)

        outer.addWidget(self.card)
        outer.addStretch()

        if text:
            self.update_text(text)

    # 🔥 NEW METHOD (IMPORTANT)
    def update_text(self, text):
        html = (
            f'<html><body style="margin:0;padding:0;color:{COLORS["text_primary"]};'
            f'font-family:Segoe UI,sans-serif;font-size:14px;line-height:1.85;">'
            + markdown_to_html(text) +
            "</body></html>"
        )
        self.browser.setHtml(html)
        self.browser.document().adjustSize()
        doc_h = int(self.browser.document().size().height())
        self.browser.setFixedHeight(doc_h + 14)


class UserBubble(QFrame):
    def __init__(self, text):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(60, 8, 60, 8)
        outer.setAlignment(Qt.AlignRight)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setMaximumWidth(520)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setStyleSheet(
            f"background-color:{COLORS['user_bubble']};color:{COLORS['text_primary']};" +
            f"padding:13px 18px;border-radius:18px;font-size:14px;" +
            f"font-family:'Segoe UI',sans-serif;line-height:1.65;border:1px solid {COLORS['border']};"
        )
        outer.addStretch()
        outer.addWidget(label)


class WorkerThread(QThread):
    finished = pyqtSignal(str)
    def __init__(self, question):
        super().__init__()
        self.question = question
    def run(self):
        response = ask_llm(self.question)
        self.finished.emit(response)


class AutoResizeTextEdit(QTextEdit):
    returnPressed = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumHeight(44)
        self.setMaximumHeight(140)
        self.document().contentsChanged.connect(self._adjust)
    def _adjust(self):
        h = int(self.document().size().height())
        self.setFixedHeight(max(44, min(h + 20, 140)))
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() & Qt.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.returnPressed.emit()
        else:
            super().keyPressEvent(event)


class ChatbotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Talkly")
        self.setMinimumSize(740, 660)
        self.resize(880, 760)
        self.setStyleSheet(
            f"QWidget {{background-color:{COLORS['bg_primary']};color:{COLORS['text_primary']};}} " +
            f"QScrollArea {{border:none;background:{COLORS['bg_primary']};}} " +
            f"QScrollBar:vertical {{background:transparent;width:5px;margin:0;}} " +
            f"QScrollBar::handle:vertical {{background:{COLORS['border']};border-radius:2px;min-height:20px;}} " +
            "QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {height:0;}"
        )
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(54)
        header.setStyleSheet(f"background:{COLORS['bg_primary']};border-bottom:1px solid {COLORS['border']};")
        h_row = QHBoxLayout(header)
        h_row.setContentsMargins(24, 0, 24, 0)
        title = QLabel("Talkly")
        title.setStyleSheet(f"color:{COLORS['text_primary']};font-size:15px;font-weight:700;letter-spacing:0.5px;")
        h_row.addWidget(title)
        h_row.addStretch()
        model_tag = QLabel("Groq \u00b7 LLaMA")
        model_tag.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;padding:3px 10px;border:1px solid {COLORS['border']};border-radius:8px;")
        h_row.addWidget(model_tag)
        root.addWidget(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet(f"background:{COLORS['bg_primary']};")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(4)
        self.chat_layout.setContentsMargins(0, 24, 0, 24)
        self.scroll.setWidget(self.chat_container)
        root.addWidget(self.scroll, stretch=1)
        self._show_welcome()

        input_wrapper = QFrame()
        input_wrapper.setStyleSheet(f"background:{COLORS['bg_primary']};border-top:1px solid {COLORS['border']};")
        input_outer = QVBoxLayout(input_wrapper)
        input_outer.setContentsMargins(60, 14, 60, 18)
        input_outer.setSpacing(8)

        input_frame = QFrame()
        input_frame.setStyleSheet(f"background:{COLORS['input_bg']};border-radius:18px;border:1px solid {COLORS['border']};")
        input_inner = QHBoxLayout(input_frame)
        input_inner.setContentsMargins(18, 8, 10, 8)
        input_inner.setSpacing(8)

        self.input_box = AutoResizeTextEdit()
        self.input_box.setPlaceholderText("Message Talkly...")
        self.input_box.setStyleSheet(f"QTextEdit {{background:transparent;color:{COLORS['text_primary']};font-size:14px;border:none;padding:4px 0;font-family:'Segoe UI',sans-serif;}}")
        self.input_box.returnPressed.connect(self.send_message)
        input_inner.addWidget(self.input_box)

        btn_col = QVBoxLayout()
        btn_col.setAlignment(Qt.AlignBottom)
        self.send_btn = QPushButton("\u2191")
        self.send_btn.setFixedSize(36, 36)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet(
            f"QPushButton {{background:{COLORS['send_btn']};color:{COLORS['send_btn_text']};border-radius:18px;font-size:17px;font-weight:bold;border:none;}}" +
            f"QPushButton:hover {{background:{COLORS['send_hover']};}}QPushButton:pressed {{background:#aaa;}}"
        )
        self.send_btn.clicked.connect(self.send_message)
        btn_col.addWidget(self.send_btn)
        input_inner.addLayout(btn_col)
        input_outer.addWidget(input_frame)

        toolbar = QHBoxLayout()
        self.upload_btn = QPushButton("\U0001f4ce  Attach PDF")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet(
            f"QPushButton {{background:transparent;color:{COLORS['text_dim']};font-size:12px;border:1px solid {COLORS['border']};border-radius:8px;padding:4px 10px;}}" +
            f"QPushButton:hover {{color:{COLORS['text_secondary']};border-color:{COLORS['text_dim']};}}"
        )
        self.upload_btn.clicked.connect(self.upload_pdf)
        toolbar.addWidget(self.upload_btn)
        toolbar.addStretch()
        hint = QLabel("Shift+Enter for new line")
        hint.setStyleSheet(f"color:{COLORS['text_dim']};font-size:11px;")
        toolbar.addWidget(hint)
        input_outer.addLayout(toolbar)
        root.addWidget(input_wrapper)

    def _show_welcome(self):
        wrap = QWidget()
        wrap.setStyleSheet("background:transparent;")
        wl = QVBoxLayout(wrap)
        wl.setAlignment(Qt.AlignCenter)
        wl.setContentsMargins(40, 80, 40, 20)
        logo = QLabel("\u2736")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:36px;")
        wl.addWidget(logo)
        greeting = QLabel("How can I help you today?")
        greeting.setAlignment(Qt.AlignCenter)
        greeting.setStyleSheet(f"color:{COLORS['text_primary']};font-size:23px;font-weight:700;margin-top:14px;")
        wl.addWidget(greeting)
        sub = QLabel("Ask anything \u2014 code, lists, and explanations are formatted clearly.")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{COLORS['text_dim']};font-size:13px;margin-top:6px;")
        wl.addWidget(sub)
        self.welcome_widget = wrap
        self.chat_layout.addWidget(wrap)

    def _remove_welcome(self):
        if hasattr(self, "welcome_widget") and self.welcome_widget:
            self.welcome_widget.setParent(None)
            self.welcome_widget = None

    def send_message(self):
        question = self.input_box.toPlainText().strip()
        if not question:
            return
        self._remove_welcome()
        self.chat_layout.addWidget(UserBubble(question))
        self.input_box.clear()
        self.input_box.setFixedHeight(44)
        self.thinking_bubble = ThinkingBubble()
        self.chat_layout.addWidget(self.thinking_bubble)
        self.auto_scroll()
        self.thread = WorkerThread(question)
        self.thread.finished.connect(self.display_response)
        self.thread.start()

    def display_response(self, response):
        # Stop thinking animation
        self.thinking_bubble.stop()
        self.thinking_bubble.setParent(None)

        # 🔥 Create empty bot widget
        self.current_bot = BotReplyWidget("")
        self.chat_layout.addWidget(self.current_bot)

        # 🔥 Prepare streaming
        self.words = response.split()
        self.current_text = ""
        self.index = 0

        self.stream_timer = QTimer()
        self.stream_timer.timeout.connect(self.stream_step)
        self.stream_timer.start(25)  # speed (lower = faster)

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self._remove_welcome()
            result = load_pdf(file_path)
            self.chat_layout.addWidget(UserBubble(f"\U0001f4c4 {file_path.split('/')[-1]}"))
            self.chat_layout.addWidget(BotReplyWidget(result))
            self.auto_scroll()

    def auto_scroll(self):
        QTimer.singleShot(60, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        ))
    
    def stream_step(self):
        if self.index < len(self.words):
            self.current_text += self.words[self.index] + " "
            self.current_bot.update_text(self.current_text)
            self.index += 1
            self.auto_scroll()
        else:
            self.stream_timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS["bg_primary"]))
    palette.setColor(QPalette.WindowText, QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.Base, QColor(COLORS["bg_secondary"]))
    palette.setColor(QPalette.Text, QColor(COLORS["text_primary"]))
    app.setPalette(palette)
    window = ChatbotUI()
    window.show()
    sys.exit(app.exec_())