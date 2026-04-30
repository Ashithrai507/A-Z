"""
PaperAI Qt UI layer.
Contains all widgets, styles, and UI event handlers.
"""

from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QFileDialog, QProgressBar, QMessageBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer

import config
from core.paperai_core import ProcessingThread, QueryThread, create_app_context


# ─── STYLE CONSTANTS ──────────────────────────────────────────────────────────

DARK_BG = "#0d0f14"
SIDEBAR_BG = "#13161e"
BUBBLE_USER = "#1e3a5f"
BUBBLE_BOT = "#1a1d27"
ACCENT = "#4f8ef7"
ACCENT_HOVER = "#6aa3ff"
TEXT_PRIMARY = "#e8ecf4"
TEXT_SECONDARY = "#7a8499"
BORDER = "#252a38"
SUCCESS = "#3dd68c"
WARNING = "#f5a623"
INPUT_BG = "#1a1d27"
SCROLLBAR_BG = "#1a1d27"
SCROLLBAR_FG = "#2e3347"

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'SF Pro Text', sans-serif;
    font-size: 13px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {SCROLLBAR_BG};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {SCROLLBAR_FG};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    height: 0px;
}}
QToolTip {{
    background-color: {SIDEBAR_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
}}
"""

SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid {BORDER};
}}
"""

BTN_PRIMARY = f"""
QPushButton {{
    background-color: {ACCENT};
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {ACCENT_HOVER};
}}
QPushButton:pressed {{
    background-color: #3a72d4;
}}
QPushButton:disabled {{
    background-color: #2a2f42;
    color: {TEXT_SECONDARY};
}}
"""

BTN_GHOST = f"""
QPushButton {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 9px 16px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {BUBBLE_BOT};
    color: {TEXT_PRIMARY};
    border-color: {ACCENT};
}}
QPushButton:pressed {{
    background-color: #1e2130;
}}
"""

BTN_SIDEBAR = f"""
QPushButton {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    text-align: left;
}}
QPushButton:hover {{
    background-color: {BUBBLE_BOT};
    color: {TEXT_PRIMARY};
}}
QPushButton:checked {{
    background-color: #1e2643;
    color: {ACCENT};
    font-weight: 600;
}}
"""

INPUT_STYLE = f"""
QLineEdit, QTextEdit {{
    background-color: {INPUT_BG};
    color: {TEXT_PRIMARY};
    border: 1.5px solid {BORDER};
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus, QTextEdit:focus {{
    border-color: {ACCENT};
    background-color: #1e2130;
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {TEXT_SECONDARY};
}}
"""

PROGRESS_STYLE = f"""
QProgressBar {{
    background-color: {BORDER};
    border: none;
    border-radius: 4px;
    height: 4px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {ACCENT}, stop:1 {ACCENT_HOVER});
    border-radius: 4px;
}}
"""


# ─── CHAT UI ELEMENTS ─────────────────────────────────────────────────────────

class ChatBubble(QWidget):
    def __init__(self, text: str, is_user: bool, timestamp: str = "", parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self._build(text, timestamp)

    def _build(self, text: str, timestamp: str):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(16, 6, 16, 6)
        outer.setSpacing(10)

        if self.is_user:
            outer.addStretch()

        col = QVBoxLayout()
        col.setSpacing(4)

        header = QHBoxLayout()
        header.setSpacing(8)

        avatar = QLabel()
        avatar.setFixedSize(28, 28)
        if self.is_user:
            avatar.setText("You")
            avatar.setAlignment(Qt.AlignCenter)
            avatar.setStyleSheet("""
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #4f8ef7, stop:1 #2563c4);
                border-radius: 14px;
                color: white;
                font-size: 9px;
                font-weight: 700;
            """)
        else:
            avatar.setText("AI")
            avatar.setAlignment(Qt.AlignCenter)
            avatar.setStyleSheet("""
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #3dd68c, stop:1 #22a866);
                border-radius: 14px;
                color: white;
                font-size: 9px;
                font-weight: 700;
            """)

        name = QLabel("You" if self.is_user else "PaperAI")
        name.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px; font-weight: 600;")

        ts = QLabel(timestamp)
        ts.setStyleSheet("color: #3d4458; font-size: 10px;")

        header.addWidget(avatar)
        header.addWidget(name)
        header.addWidget(ts)
        header.addStretch()

        bubble = QLabel()
        bubble.setText(text)
        bubble.setWordWrap(True)
        bubble.setTextFormat(Qt.RichText)
        bubble.setOpenExternalLinks(False)
        bubble.setMaximumWidth(620)
        bubble.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        bg = BUBBLE_USER if self.is_user else BUBBLE_BOT
        radius_tl = "4px" if self.is_user else "16px"
        radius_tr = "16px" if self.is_user else "4px"

        bubble.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {TEXT_PRIMARY};
                border-radius: 16px;
                border-top-left-radius: {radius_tl};
                border-top-right-radius: {radius_tr};
                padding: 12px 16px;
                font-size: 13px;
                line-height: 1.6;
            }}
        """)

        col.addLayout(header)
        col.addWidget(bubble, alignment=Qt.AlignLeft if not self.is_user else Qt.AlignRight)

        outer.addLayout(col)
        if not self.is_user:
            outer.addStretch()


class TypingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._dots = 0

    def _setup(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)
        layout.setSpacing(10)

        avatar = QLabel("AI")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #3dd68c, stop:1 #22a866);
            border-radius: 14px; color: white;
            font-size: 9px; font-weight: 700;
        """)

        self._label = QLabel("PaperAI is thinking")
        self._label.setStyleSheet(f"""
            background-color: {BUBBLE_BOT};
            color: {TEXT_SECONDARY};
            border-radius: 16px;
            border-top-left-radius: 4px;
            padding: 12px 16px;
            font-size: 13px;
            font-style: italic;
        """)

        layout.addWidget(avatar)
        layout.addWidget(self._label)
        layout.addStretch()

    def start(self):
        self._timer.start(400)
        self.show()

    def stop(self):
        self._timer.stop()
        self.hide()

    def _tick(self):
        self._dots = (self._dots + 1) % 4
        self._label.setText("PaperAI is thinking" + "." * self._dots)


# ─── MAIN WINDOW ──────────────────────────────────────────────────────────────

class PaperAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaperAI — Research Paper Assistant")
        self.setGeometry(100, 80, 1260, 820)
        self.setMinimumSize(900, 600)

        self.app_context = create_app_context()
        self.processing_thread = None
        self.query_thread = None
        self._current_mode = "qa"
        self._pdf_loaded = self.app_context["vector_db"].get_size() > 0

        self.setStyleSheet(GLOBAL_STYLE)
        self._init_ui()

    # ── UI BUILD ──────────────────────────────────────────────────────────────

    def _init_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())
        root_layout.addWidget(self._build_main(), stretch=1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(4)

        logo_row = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {ACCENT}; font-size: 18px;")
        title = QLabel("PaperAI")
        title.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.5px;
        """)
        logo_row.addWidget(dot)
        logo_row.addWidget(title)
        logo_row.addStretch()
        layout.addLayout(logo_row)
        layout.addSpacing(24)

        upload_label = QLabel("DOCUMENT")
        upload_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;"
        )
        layout.addWidget(upload_label)
        layout.addSpacing(6)

        self.upload_btn = QPushButton("  📄  Upload PDF")
        self.upload_btn.setStyleSheet(BTN_PRIMARY)
        self.upload_btn.setFixedHeight(42)
        self.upload_btn.clicked.connect(self.upload_pdf)
        layout.addWidget(self.upload_btn)

        self.pdf_status_label = QLabel("No document loaded")
        self.pdf_status_label.setWordWrap(True)
        self.pdf_status_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px; padding: 6px 4px;")
        layout.addWidget(self.pdf_status_label)

        if self._pdf_loaded:
            n = self.app_context["vector_db"].get_size()
            self.pdf_status_label.setText(f"✅  {n} chunks loaded")

        self.clear_db_btn = QPushButton("  🧹  Clear Vector DB")
        self.clear_db_btn.setStyleSheet(BTN_GHOST)
        self.clear_db_btn.setFixedHeight(36)
        self.clear_db_btn.clicked.connect(self._clear_vector_db)
        layout.addWidget(self.clear_db_btn)

        layout.addSpacing(20)

        mode_label = QLabel("MODE")
        mode_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;"
        )
        layout.addWidget(mode_label)
        layout.addSpacing(6)

        self.btn_qa = QPushButton("  💬  Ask a Question")
        self.btn_concept = QPushButton("  💡  Explain Concept")
        self.btn_summarize = QPushButton("  📋  Summarize Paper")

        for btn in (self.btn_qa, self.btn_concept, self.btn_summarize):
            btn.setStyleSheet(BTN_SIDEBAR)
            btn.setCheckable(True)
            btn.setFixedHeight(40)
            btn.setAutoExclusive(True)
            layout.addWidget(btn)

        self.btn_qa.setChecked(True)
        self.btn_qa.clicked.connect(lambda: self._set_mode("qa"))
        self.btn_concept.clicked.connect(lambda: self._set_mode("concept"))
        self.btn_summarize.clicked.connect(lambda: self._set_mode("summarize"))

        layout.addStretch()

        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BUBBLE_BOT};
                border-radius: 10px;
                border: 1px solid {BORDER};
            }}
        """)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(12, 10, 12, 10)
        stats_layout.setSpacing(4)

        self.stats_label = QLabel(
            f"Vectors: {self.app_context['vector_db'].get_size()}\nModel: {config.LLM_MODEL.split('-')[0]}"
        )
        self.stats_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px; line-height: 1.6;")
        stats_layout.addWidget(self.stats_label)
        layout.addWidget(stats_frame)

        return sidebar

    def _build_main(self) -> QWidget:
        main = QWidget()
        layout = QVBoxLayout(main)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        topbar = QWidget()
        topbar.setFixedHeight(56)
        topbar.setStyleSheet(f"""
            background-color: {SIDEBAR_BG};
            border-bottom: 1px solid {BORDER};
        """)
        tb_layout = QHBoxLayout(topbar)
        tb_layout.setContentsMargins(20, 0, 20, 0)

        self.mode_title = QLabel("Ask a Question")
        self.mode_title.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 15px; font-weight: 600;")

        self.mode_hint = QLabel("Ask anything about your research paper")
        self.mode_hint.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")

        clear_btn = QPushButton("Clear Chat")
        clear_btn.setStyleSheet(BTN_GHOST)
        clear_btn.setFixedHeight(34)
        clear_btn.clicked.connect(self._clear_chat)

        tb_layout.addWidget(self.mode_title)
        tb_layout.addSpacing(14)
        tb_layout.addWidget(self.mode_hint)
        tb_layout.addStretch()
        tb_layout.addWidget(clear_btn)

        layout.addWidget(topbar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(PROGRESS_STYLE)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(f"background: {DARK_BG};")

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet(f"background: {DARK_BG};")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 16, 0, 16)
        self.chat_layout.setSpacing(4)
        self.chat_layout.addStretch()

        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        self.chat_layout.addWidget(self.typing_indicator)

        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area, stretch=1)

        self._add_bot_bubble(
            "👋 <b>Welcome to PaperAI!</b><br><br>"
            "Upload a research paper PDF using the sidebar, then:<br>"
            "• <b>Ask questions</b> — get precise answers from the paper<br>"
            "• <b>Explain concepts</b> — understand complex ideas simply<br>"
            "• <b>Summarize</b> — get a full overview instantly"
        )

        input_area = QWidget()
        input_area.setStyleSheet(f"""
            background-color: {SIDEBAR_BG};
            border-top: 1px solid {BORDER};
        """)
        ia_layout = QVBoxLayout(input_area)
        ia_layout.setContentsMargins(20, 14, 20, 16)
        ia_layout.setSpacing(10)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px;")
        ia_layout.addWidget(self.status_label)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your question here…")
        self.input_field.setStyleSheet(INPUT_STYLE)
        self.input_field.setFixedHeight(48)
        self.input_field.returnPressed.connect(self._on_send)

        self.send_btn = QPushButton("Send  ➤")
        self.send_btn.setStyleSheet(BTN_PRIMARY)
        self.send_btn.setFixedSize(100, 48)
        self.send_btn.clicked.connect(self._on_send)

        input_row.addWidget(self.input_field, stretch=1)
        input_row.addWidget(self.send_btn)
        ia_layout.addLayout(input_row)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)
        chips = [
            ("What is this paper about?", "qa"),
            ("Key contributions?", "qa"),
            ("Main methodology?", "qa"),
        ]
        for label, mode in chips:
            chip = QPushButton(label)
            chip.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {TEXT_SECONDARY};
                    border: 1px solid {BORDER};
                    border-radius: 16px;
                    padding: 5px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    border-color: {ACCENT};
                    color: {ACCENT};
                    background-color: #1a2033;
                }}
            """)
            chip.setCursor(Qt.PointingHandCursor)
            chip.clicked.connect(lambda checked, t=label, m=mode: self._chip_click(t, m))
            chips_row.addWidget(chip)
        chips_row.addStretch()
        ia_layout.addLayout(chips_row)

        layout.addWidget(input_area)
        return main

    # ── HELPERS ───────────────────────────────────────────────────────────────

    def _set_mode(self, mode: str):
        self._current_mode = mode
        titles = {
            "qa": ("Ask a Question", "Ask anything about your research paper"),
            "concept": ("Explain Concept", "Get complex ideas explained in simple language"),
            "summarize": ("Summarize Paper", "Generate a comprehensive summary of the paper"),
        }
        t, h = titles[mode]
        self.mode_title.setText(t)
        self.mode_hint.setText(h)

        if mode == "qa":
            self.input_field.setPlaceholderText("Type your question here…")
            self.input_field.setEnabled(True)
        elif mode == "concept":
            self.input_field.setPlaceholderText("Enter a concept to explain, e.g. 'Transformer architecture'…")
            self.input_field.setEnabled(True)
        else:
            self.input_field.setPlaceholderText("Click Send to summarize the loaded paper…")
            self.input_field.setEnabled(False)

    def _add_user_bubble(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        bubble = ChatBubble(text, is_user=True, timestamp=ts)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._scroll_to_bottom()

    def _add_bot_bubble(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        bubble = ChatBubble(text, is_user=False, timestamp=ts)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def _clear_chat(self):
        while self.chat_layout.count() > 2:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._add_bot_bubble("🗑️ Chat cleared. Ready for a new session!")

    def _clear_vector_db(self):
        if self.app_context["vector_db"].get_size() == 0:
            self._add_bot_bubble("ℹ️ Vector DB is already empty.")
            return

        confirm = QMessageBox.question(
            self,
            "Clear Vector DB",
            "This will delete all stored vectors and metadata. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        self.app_context["vector_db"].reset()
        db_path = Path(config.VECTOR_DB_PATH)
        (db_path / "index.faiss").unlink(missing_ok=True)
        (db_path / "metadata.pkl").unlink(missing_ok=True)

        self._pdf_loaded = False
        self.pdf_status_label.setText("No document loaded")
        self.stats_label.setText(f"Vectors: 0\nModel: {config.LLM_MODEL.split('-')[0]}")
        self._add_bot_bubble("✅ Vector database cleared. Upload a new PDF to start.")

    def _set_busy(self, busy: bool):
        self.send_btn.setEnabled(not busy)
        self.input_field.setEnabled(not busy and self._current_mode != "summarize")
        self.upload_btn.setEnabled(not busy)
        self.progress_bar.setVisible(busy)
        if busy:
            self.typing_indicator.start()
        else:
            self.typing_indicator.stop()

    def _chip_click(self, text: str, mode: str):
        if not self._pdf_loaded:
            self._add_bot_bubble("⚠️ Please upload a PDF first using the sidebar.")
            return
        self._set_mode(mode)
        if mode == "qa":
            self.btn_qa.setChecked(True)
        self.input_field.setText(text)
        self._on_send()

    # ── ACTIONS ───────────────────────────────────────────────────────────────

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return
        if not config.GROQ_API_KEY:
            self._add_bot_bubble("❌ <b>GROQ_API_KEY not set.</b> Please add it to your <code>.env</code> file.")
            return

        fname = Path(file_path).name
        self._add_user_bubble(f"📄 Uploading: <b>{fname}</b>")
        self._add_bot_bubble(f"Processing <b>{fname}</b>… This may take a moment.")
        self._set_busy(True)
        self.status_label.setText("Processing PDF…")

        self.processing_thread = ProcessingThread(file_path, self.app_context)
        self.processing_thread.progress.connect(lambda msg: self.status_label.setText(msg))
        self.processing_thread.finished.connect(self._on_pdf_done)
        self.processing_thread.start()

    def _on_pdf_done(self, success: bool, message: str):
        self._set_busy(False)
        self.status_label.setText("")
        if success:
            self._pdf_loaded = True
            n = self.app_context["vector_db"].get_size()
            self.pdf_status_label.setText(f"✅  {n} chunks loaded")
            self.stats_label.setText(f"Vectors: {n}\nModel: {config.LLM_MODEL.split('-')[0]}")
            self._add_bot_bubble(f"✅ <b>PDF processed successfully!</b><br>{message.replace(chr(10), '<br>')}")
        else:
            self._add_bot_bubble(f"❌ <b>Processing failed.</b><br>{message}")

    def _on_send(self):
        mode = self._current_mode

        if mode != "summarize":
            query = self.input_field.text().strip()
            if not query:
                return
        else:
            query = ""

        if not self._pdf_loaded:
            self._add_bot_bubble("⚠️ Please upload a PDF first using the sidebar.")
            return

        if mode == "summarize":
            self._add_user_bubble("📋 Generate a summary of the paper")
        else:
            self._add_user_bubble(query)
            self.input_field.clear()

        self._set_busy(True)
        self.status_label.setText("Thinking…")

        self.query_thread = QueryThread(query, mode, self.app_context)
        self.query_thread.finished.connect(self._on_query_done)
        self.query_thread.error.connect(self._on_query_error)
        self.query_thread.start()

    def _on_query_done(self, result: str):
        self._set_busy(False)
        self.status_label.setText("")
        html_result = result.replace("\n", "<br>")
        self._add_bot_bubble(html_result)

    def _on_query_error(self, error: str):
        self._set_busy(False)
        self.status_label.setText("")
        self._add_bot_bubble(f"❌ <b>Error:</b> {error}")
