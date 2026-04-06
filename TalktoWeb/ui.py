import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation,
    QEasingCurve, QSize, QPoint, pyqtProperty, QRect
)
from PyQt5.QtGui import (
    QColor, QFont, QPainter, QBrush, QPen, QLinearGradient,
    QFontDatabase, QPalette, QPixmap, QIcon, QTextCursor,
    QRadialGradient
)


# ─────────────────────────────────────────────
#  COLORS  (Claude-inspired dark palette)
# ─────────────────────────────────────────────
BG_DEEP       = "#0f0f0f"
BG_PANEL      = "#1a1a1a"
BG_INPUT      = "#242424"
BG_USER_MSG   = "#2a2a2a"
BG_BOT_MSG    = "#1e1e1e"
ACCENT        = "#cc785c"      # Claude's signature warm orange
ACCENT_LIGHT  = "#e8956d"
TEXT_PRIMARY  = "#e8e6e0"
TEXT_SECONDARY= "#9b9890"
TEXT_MUTED    = "#5c5a56"
BORDER        = "#2e2e2e"
BORDER_LIGHT  = "#3a3a3a"
HOVER_BG      = "#2f2f2f"
SEND_BG       = "#cc785c"
SEND_HOVER    = "#d4845e"


# ─────────────────────────────────────────────
#  TYPING DOTS ANIMATION WIDGET
# ─────────────────────────────────────────────
class TypingDotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 28)
        self._phase = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.setInterval(60)
        self._active = False

    def start(self):
        self._active = True
        self._phase = 0.0
        self._timer.start()
        self.show()

    def stop(self):
        self._active = False
        self._timer.stop()
        self.hide()

    def _tick(self):
        self._phase = (self._phase + 0.12) % (3.14159 * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        import math
        cx = [10, 26, 42]
        cy = 14
        for i, x in enumerate(cx):
            offset = math.sin(self._phase - i * 1.1) * 4
            alpha = int(160 + 80 * math.sin(self._phase - i * 1.1))
            alpha = max(80, min(255, alpha))
            color = QColor(ACCENT)
            color.setAlpha(alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(x, int(cy + offset)), 4, 4)


# ─────────────────────────────────────────────
#  SINGLE MESSAGE BUBBLE
# ─────────────────────────────────────────────
class MessageBubble(QFrame):
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self._setup_ui(text)

    def _setup_ui(self, text):
        self.setFrameShape(QFrame.NoFrame)
        outer = QHBoxLayout(self)
        outer.setContentsMargins(24, 6, 24, 6)
        outer.setSpacing(0)

        if self.is_user:
            outer.addStretch()

        # Avatar + bubble column
        col = QVBoxLayout()
        col.setSpacing(4)

        if not self.is_user:
            # Bot avatar row
            avatar_row = QHBoxLayout()
            avatar_row.setSpacing(10)
            avatar = self._make_avatar()
            name_lbl = QLabel("VCET Assistant")
            name_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px; font-weight: 600; letter-spacing: 0.5px;")
            avatar_row.addWidget(avatar)
            avatar_row.addWidget(name_lbl)
            avatar_row.addStretch()
            col.addLayout(avatar_row)

        # Bubble
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        max_w = 680 if not self.is_user else 520
        bubble.setMaximumWidth(max_w)

        if self.is_user:
            bubble.setStyleSheet(f"""
                QLabel {{
                    background-color: {BG_USER_MSG};
                    color: {TEXT_PRIMARY};
                    border: 1px solid {BORDER_LIGHT};
                    border-radius: 18px;
                    border-bottom-right-radius: 4px;
                    padding: 12px 16px;
                    font-size: 14px;
                    line-height: 1.6;
                }}
            """)
        else:
            bubble.setStyleSheet(f"""
                QLabel {{
                    background-color: transparent;
                    color: {TEXT_PRIMARY};
                    border-radius: 0px;
                    padding: 4px 0px;
                    font-size: 14px;
                    line-height: 1.6;
                }}
            """)

        col.addWidget(bubble)
        outer.addLayout(col)

        if self.is_user:
            pass
        else:
            outer.addStretch()

    def _make_avatar(self):
        lbl = QLabel()
        lbl.setFixedSize(28, 28)
        lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {ACCENT};
                border-radius: 14px;
                color: white;
                font-size: 11px;
                font-weight: 700;
            }}
        """)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setText("V")
        return lbl


# ─────────────────────────────────────────────
#  TYPING INDICATOR ROW
# ─────────────────────────────────────────────
class TypingIndicator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 6, 24, 6)

        inner = QHBoxLayout()
        inner.setSpacing(10)

        avatar = QLabel()
        avatar.setFixedSize(28, 28)
        avatar.setStyleSheet(f"""
            QLabel {{
                background-color: {ACCENT};
                border-radius: 14px;
                color: white;
                font-size: 11px;
                font-weight: 700;
            }}
        """)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setText("V")

        self.dots = TypingDotsWidget()

        inner.addWidget(avatar)
        inner.addWidget(self.dots)
        inner.addStretch()

        layout.addLayout(inner)
        layout.addStretch()
        self.hide()

    def start(self):
        self.dots.start()
        self.show()

    def stop(self):
        self.dots.stop()
        self.hide()


# ─────────────────────────────────────────────
#  LOADING SCREEN (shown while indexing)
# ─────────────────────────────────────────────
class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {BG_DEEP};")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Spinner
        self.spinner = SpinnerWidget()
        layout.addWidget(self.spinner, 0, Qt.AlignCenter)

        self.title = QLabel("Indexing College Website")
        self.title.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 20px; font-weight: 600;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.subtitle = QLabel("Crawling pages and building knowledge base...")
        self.subtitle.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)

        self.hide()

    def start(self, msg="Crawling pages and building knowledge base..."):
        self.subtitle.setText(msg)
        self.spinner.start()
        self.show()
        self.raise_()

    def stop(self):
        self.spinner.stop()
        self.hide()


class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(56, 56)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._timer.setInterval(16)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _rotate(self):
        self._angle = (self._angle + 4) % 360
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(28, 28)
        painter.rotate(self._angle)

        pen = QPen(QColor(ACCENT), 3.5, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)

        import math
        for i in range(10):
            alpha = int(255 * (i / 10) ** 1.5)
            c = QColor(ACCENT)
            c.setAlpha(alpha)
            pen.setColor(c)
            painter.setPen(pen)
            a1 = -i * 36
            a2 = a1 - 28
            painter.drawArc(-22, -22, 44, 44, a1 * 16, (a2 - a1) * 16)


# ─────────────────────────────────────────────
#  CUSTOM SEND BUTTON
# ─────────────────────────────────────────────
class SendButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self._hovered = False
        self.setStyleSheet("background: transparent; border: none;")

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bg = QColor(SEND_HOVER if self._hovered else SEND_BG)
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 36, 36)

        # Arrow icon
        painter.setPen(QPen(QColor("white"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(14, 20, 26, 20)
        painter.drawLine(21, 14, 27, 20)
        painter.drawLine(21, 26, 27, 20)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
class Sidebar(QWidget):
    load_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setStyleSheet(f"background-color: {BG_PANEL};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)

        # Logo area
        logo_row = QHBoxLayout()
        logo_dot = QLabel()
        logo_dot.setFixedSize(28, 28)
        logo_dot.setStyleSheet(f"""
            QLabel {{
                background-color: {ACCENT};
                border-radius: 8px;
                color: white;
                font-size: 13px;
                font-weight: 800;
            }}
        """)
        logo_dot.setAlignment(Qt.AlignCenter)
        logo_dot.setText("V")

        logo_text = QLabel("VCET Bot")
        logo_text.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        logo_row.addWidget(logo_dot)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        layout.addLayout(logo_row)

        layout.addSpacing(24)

        # New chat button
        new_btn = QPushButton("+ New Chat")
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXT_PRIMARY};
                border: 1px solid {BORDER_LIGHT};
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 500;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {HOVER_BG};
                border-color: {TEXT_MUTED};
            }}
        """)
        layout.addWidget(new_btn)

        layout.addSpacing(8)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"color: {BORDER};")
        layout.addWidget(div)

        layout.addSpacing(8)

        section = QLabel("TOOLS")
        section.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(section)

        # Load data button
        self.load_btn = QPushButton("⟳  Load College Data")
        self.load_btn.setCursor(Qt.PointingHandCursor)
        self.load_btn.clicked.connect(self.load_clicked.emit)
        self.load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 600;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_LIGHT};
            }}
        """)
        layout.addWidget(self.load_btn)

        # Status label
        self.status_lbl = QLabel("Not loaded")
        self.status_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; padding-left: 4px;")
        layout.addWidget(self.status_lbl)

        layout.addSpacing(16)

        div2 = QFrame()
        div2.setFrameShape(QFrame.HLine)
        div2.setStyleSheet(f"color: {BORDER};")
        layout.addWidget(div2)

        layout.addSpacing(8)

        section2 = QLabel("TOPICS")
        section2.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(section2)

        topics = ["Departments", "Admissions", "Faculty", "Fees & Aid", "Placements", "Contact"]
        for t in topics:
            btn = QPushButton(t)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {TEXT_SECONDARY};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 10px;
                    font-size: 13px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {HOVER_BG};
                    color: {TEXT_PRIMARY};
                }}
            """)
            layout.addWidget(btn)

        layout.addStretch()

        # Version
        ver = QLabel("VCET Chatbot v2.0")
        ver.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px;")
        layout.addWidget(ver)

    def set_status(self, text, ok=True):
        color = "#5cb85c" if ok else ACCENT
        self.status_lbl.setStyleSheet(f"color: {color}; font-size: 11px; padding-left: 4px;")
        self.status_lbl.setText(text)


# ─────────────────────────────────────────────
#  WORKER THREAD (for LLM + loading)
# ─────────────────────────────────────────────
class WorkerThread(QThread):
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, fn, *args):
        super().__init__()
        self._fn = fn
        self._args = args

    def run(self):
        try:
            result = self._fn(*self._args)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VCET College Chatbot")
        self.setMinimumSize(900, 640)
        self.resize(1100, 720)
        self._setup_palette()
        self._setup_ui()
        self._show_welcome()

    def _setup_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(BG_DEEP))
        palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
        palette.setColor(QPalette.Base, QColor(BG_INPUT))
        palette.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
        self.setPalette(palette)
        self.setStyleSheet(f"QMainWindow {{ background-color: {BG_DEEP}; }}")

    def _setup_ui(self):
        central = QWidget()
        central.setStyleSheet(f"background-color: {BG_DEEP};")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──
        self.sidebar = Sidebar()
        self.sidebar.load_clicked.connect(self._on_load_data)
        main_layout.addWidget(self.sidebar)

        # ── Vertical separator ──
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background-color: {BORDER};")
        main_layout.addWidget(sep)

        # ── Chat area ──
        chat_area = QWidget()
        chat_area.setStyleSheet(f"background-color: {BG_DEEP};")
        chat_col = QVBoxLayout(chat_area)
        chat_col.setContentsMargins(0, 0, 0, 0)
        chat_col.setSpacing(0)

        # Header
        header = self._build_header()
        chat_col.addWidget(header)

        # Messages scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {BG_DEEP}; }}
            QScrollBar:vertical {{
                background: transparent; width: 6px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER_LIGHT}; border-radius: 3px; min-height: 40px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        self.messages_widget = QWidget()
        self.messages_widget.setStyleSheet(f"background-color: {BG_DEEP};")
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 16, 0, 16)
        self.messages_layout.setSpacing(2)
        self.messages_layout.addStretch()

        self.scroll.setWidget(self.messages_widget)
        chat_col.addWidget(self.scroll, 1)

        # Typing indicator
        self.typing_indicator = TypingIndicator()
        chat_col.addWidget(self.typing_indicator)

        # Input area
        input_area = self._build_input_area()
        chat_col.addWidget(input_area)

        main_layout.addWidget(chat_area, 1)

        # Loading overlay (on top)
        self.loading_overlay = LoadingOverlay(central)
        self.loading_overlay.setGeometry(central.rect())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.setGeometry(self.centralWidget().rect())

    def _build_header(self):
        header = QWidget()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            background-color: {BG_PANEL};
            border-bottom: 1px solid {BORDER};
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QLabel("VCET Puttur  ·  College Assistant")
        title.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 15px; font-weight: 600;")
        layout.addWidget(title)
        layout.addStretch()

        self.model_badge = QLabel("llama-3.3-70b")
        self.model_badge.setStyleSheet(f"""
            QLabel {{
                color: {ACCENT};
                background-color: rgba(204,120,92,0.12);
                border: 1px solid rgba(204,120,92,0.3);
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(self.model_badge)
        return header

    def _build_input_area(self):
        container = QWidget()
        container.setStyleSheet(f"background-color: {BG_DEEP};")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(48, 12, 48, 20)
        layout.setSpacing(0)

        # Input row
        row = QWidget()
        row.setStyleSheet(f"""
            background-color: {BG_INPUT};
            border: 1px solid {BORDER_LIGHT};
            border-radius: 16px;
        """)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(16, 8, 8, 8)
        row_layout.setSpacing(8)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Ask anything about VCET Puttur...")
        self.input_field.setFixedHeight(48)
        self.input_field.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input_field.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                border: none;
                color: {TEXT_PRIMARY};
                font-size: 14px;
                padding-top: 8px;
            }}
        """)
        self.input_field.installEventFilter(self)

        self.send_btn = SendButton()
        self.send_btn.clicked.connect(self._send_message)

        row_layout.addWidget(self.input_field)
        row_layout.addWidget(self.send_btn, 0, Qt.AlignBottom)
        layout.addWidget(row)

        hint = QLabel("VCET Chatbot may make mistakes. Verify important information.")
        hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addSpacing(6)
        layout.addWidget(hint)

        return container

    def eventFilter(self, obj, event):
        from PyQt5.QtCore import QEvent
        if obj is self.input_field and event.type() == QEvent.KeyPress:
            from PyQt5.QtGui import QKeyEvent
            if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
                self._send_message()
                return True
        return super().eventFilter(obj, event)

    def _show_welcome(self):
        welcome = QWidget()
        welcome.setStyleSheet(f"background: transparent;")
        wl = QVBoxLayout(welcome)
        wl.setAlignment(Qt.AlignCenter)
        wl.setSpacing(12)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(64, 64)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {ACCENT};
                border-radius: 18px;
                color: white;
                font-size: 28px;
                font-weight: 800;
            }}
        """)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setText("V")

        h1 = QLabel("How can I help you?")
        h1.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 26px; font-weight: 700;")
        h1.setAlignment(Qt.AlignCenter)

        h2 = QLabel("Ask me anything about VCET Puttur — departments, admissions, faculty, placements and more.")
        h2.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px;")
        h2.setAlignment(Qt.AlignCenter)
        h2.setWordWrap(True)

        # Suggestion chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(10)
        chips_row.setAlignment(Qt.AlignCenter)
        suggestions = ["What departments exist?", "Admission requirements", "Faculty info", "Placement stats"]
        for s in suggestions:
            chip = QPushButton(s)
            chip.setCursor(Qt.PointingHandCursor)
            chip.clicked.connect(lambda _, t=s: self._inject_suggestion(t))
            chip.setStyleSheet(f"""
                QPushButton {{
                    background-color: {BG_INPUT};
                    color: {TEXT_SECONDARY};
                    border: 1px solid {BORDER_LIGHT};
                    border-radius: 20px;
                    padding: 8px 14px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {HOVER_BG};
                    color: {TEXT_PRIMARY};
                    border-color: {TEXT_MUTED};
                }}
            """)
            chips_row.addWidget(chip)

        wl.addWidget(icon_lbl, 0, Qt.AlignCenter)
        wl.addWidget(h1)
        wl.addWidget(h2)
        wl.addSpacing(16)
        wl.addLayout(chips_row)

        # Insert before the stretch
        self.messages_layout.insertWidget(0, welcome)
        self.welcome_widget = welcome

    def _inject_suggestion(self, text):
        self.input_field.setPlainText(text)
        self._send_message()

    def _add_message(self, text, is_user=False):
        bubble = MessageBubble(text, is_user)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        QTimer.singleShot(50, self._scroll_to_bottom)
        return bubble

    def _scroll_to_bottom(self):
        sb = self.scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _send_message(self):
        text = self.input_field.toPlainText().strip()
        if not text:
            return

        # Remove welcome screen on first message
        if hasattr(self, 'welcome_widget') and self.welcome_widget is not None:
            self.welcome_widget.hide()
            self.messages_layout.removeWidget(self.welcome_widget)
            self.welcome_widget.deleteLater()
            self.welcome_widget = None

        self.input_field.clear()
        self._add_message(text, is_user=True)
        self.typing_indicator.start()
        self.send_btn.setEnabled(False)

        # Run ask_llm in thread
        self._worker = WorkerThread(self._ask, text)
        self._worker.result_ready.connect(self._on_response)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def _ask(self, text):
        from main import ask_llm
        return ask_llm(text)

    def _on_response(self, text):
        self.typing_indicator.stop()
        self.send_btn.setEnabled(True)
        self._add_message(text, is_user=False)

    def _on_error(self, err):
        self.typing_indicator.stop()
        self.send_btn.setEnabled(True)
        self._add_message(f"⚠ Error: {err}", is_user=False)

    def _on_load_data(self):
        self.loading_overlay.start("Crawling VCET website and building knowledge base...")
        self.sidebar.set_status("Loading...", ok=False)

        self._load_worker = WorkerThread(self._do_load)
        self._load_worker.result_ready.connect(self._on_loaded)
        self._load_worker.error_occurred.connect(self._on_load_error)
        self._load_worker.start()

    def _do_load(self):
        from main import load_college_data
        return load_college_data()

    def _on_loaded(self, msg):
        self.loading_overlay.stop()
        self.sidebar.set_status("✓ Data loaded", ok=True)
        self._add_message(f"**Knowledge base ready!**\n\n{msg}\n\nYou can now ask me anything about VCET Puttur.", is_user=False)

    def _on_load_error(self, err):
        self.loading_overlay.stop()
        self.sidebar.set_status("Load failed", ok=False)
        self._add_message(f"⚠ Failed to load data: {err}", is_user=False)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HAMZA-GPT")

    # Try to load a nice font
    QFontDatabase.addApplicationFont(":/fonts/Geist-Regular.ttf")
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)

    win = ChatWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()