from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer

from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = f"{current_dir}\Frontend\Graphics"

# Enhanced color palette
COLORS = {
    'primary_bg': '#0F1419',          # Deep dark blue-black
    'secondary_bg': '#1A1F2E',        # Dark slate
    'accent_bg': '#252A3A',           # Medium dark
    'primary_text': '#00E5FF',        # Bright cyan
    'secondary_text': '#B0BEC5',      # Light gray-blue
    'white_text': '#FFFFFF',          # Pure white
    'success': '#4CAF50',             # Green
    'warning': '#FF9800',             # Orange
    'error': '#F44336',               # Red
    'border': 'rgba(0, 229, 255, 0.3)', # Cyan with transparency
    'hover': 'rgba(0, 229, 255, 0.1)',  # Cyan hover effect
}

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', ',', ';', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['?', ',', ';', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(f'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path

def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    
    def __init__(self):
        super(ChatSection, self).__init__()
        
        # Main layout with responsive margins
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 30, 25, 30)
        layout.setSpacing(20)

        # Chat text area with enhanced scrolling
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        # Modern font setup
        font = QFont("Segoe UI", 12)
        font.setWeight(QFont.Normal)
        self.chat_text_edit.setFont(font)
        
        # Enhanced text color formatting
        text_color = QColor(COLORS['primary_text'])
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)

        # Bottom section container for GIF and status
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 10, 0, 10)
        bottom_layout.setSpacing(20)

        # Status label - positioned on the left
        self.label = QLabel("")
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary_text']}; 
                font-size: 16px; 
                font-family: 'Segoe UI', Arial;
                font-weight: bold;
                border: 2px solid rgba(0, 229, 255, 0.3); 
                background: rgba(0, 229, 255, 0.08);
                border-radius: 10px;
                margin-bottom: 50px;
                padding: 8px 15px;
                min-width: 150px;
                max-height: 40px;
            }}
        """)
        self.label.setAlignment(Qt.AlignCenter)
        
        # GIF section - positioned on the right
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {COLORS['border']};
                border-radius: 15px;
                background: rgba(0, 0, 0, 0.3);
                padding: 5px;
                margin-bottom: 50px;
            }}
        """)
        
        movie = QMovie(GraphicsDirectoryPath('Rightly.gif'))
        # Responsive GIF sizing
        max_gif_size_W = 360
        max_gif_size_H = 200
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setMovie(movie)
        movie.start()
        
        # Add widgets to bottom layout
        bottom_layout.addWidget(self.label, alignment=Qt.AlignLeft | Qt.AlignBottom)
        bottom_layout.addStretch()  # This pushes the GIF to the right
        bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)
        
        # Add bottom container to main layout
        layout.addWidget(bottom_container)

        # Layout configuration for responsiveness
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(0, 1)  # Chat area takes most space
        layout.setStretch(1, 0)  # Status container fixed size
        layout.setStretch(2, 0)  # GIF container fixed size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        
        # Event filter for enhanced interaction
        self.chat_text_edit.viewport().installEventFilter(self)
        
        # Modern theme with gradients - NO SHADOWS
        self.setStyleSheet(f"""
            ChatSection {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['primary_bg']}, 
                    stop:0.3 {COLORS['secondary_bg']}, 
                    stop:1 {COLORS['accent_bg']});
                border-radius: 10px;
            }}
            
            QTextEdit {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 31, 46, 0.95), 
                    stop:1 rgba(37, 42, 58, 0.85));
                border: 2px solid {COLORS['border']};
                border-radius: 15px;
                padding: 20px;
                color: {COLORS['primary_text']};
                font-weight: 500;
                line-height: 1.6;
                selection-background-color: rgba(0, 229, 255, 0.25);
            }}
            
            QTextEdit:focus {{
                border: 3px solid rgba(0, 229, 255, 0.8);
            }}
            
            /* Enhanced Scrollbar Design */
            QScrollBar:vertical {{
                background: rgba(15, 20, 25, 0.8);
                width: 14px;
                border-radius: 7px;
                margin: 2px;
            }}

            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary_text']}, 
                    stop:1 #0091EA);
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #40E0D0, stop:1 #00BCD4);
            }}
            
            QScrollBar::handle:vertical:pressed {{
                background: #00BCD4;
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0;
            }}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
            
            QScrollBar:horizontal {{
                background: rgba(15, 20, 25, 0.8);
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }}

            QScrollBar::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['primary_text']}, 
                    stop:1 #0091EA);
                border-radius: 7px;
                min-width: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #40E0D0, stop:1 #00BCD4);
            }}
        """)

    def loadMessages(self):
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages and len(messages) > 1 and str(old_chat_message) != str(messages):
                    self.addMessage(message=messages, color=COLORS['white_text'])
                    old_chat_message = messages
        except FileNotFoundError:
            pass
        
    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages.strip():  # Only update if there's actual content
                    self.label.setText(messages)
                else:
                    self.label.setText("Ready...")  # Default text when no status
        except FileNotFoundError:
            self.label.setText("Ready...")

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(12)
        formatm.setLeftMargin(15)
        formatm.setBottomMargin(8)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        # Auto-scroll to bottom
        scrollbar = self.chat_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class InitialScreen(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Get screen dimensions for responsive design
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Main layout with better spacing
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 60, 40, 120)
        content_layout.setSpacing(30)
        
        # Central container for better organization
        central_container = QWidget()
        central_layout = QVBoxLayout(central_container)
        central_layout.setSpacing(25)
        
        # Enhanced GIF with responsive sizing
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Rightly.gif'))
        
        # Responsive GIF sizing based on screen size
        gif_width = min(550, screen_width)
        gif_height = min(300, screen_height)
        movie.setScaledSize(QSize(gif_width, gif_height))
        
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setStyleSheet(f"""
            QLabel {{
                border: 3px solid {COLORS['border']};
                border-radius: 20px;
                background: rgba(0, 0, 0, 0.3);
                padding: 10px;
            }}
        """)
        movie.start()
        
        # Enhanced status label
        self.label = QLabel("Ready...")
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary_text']}; 
                font-size: 18px; 
                font-family: 'Segoe UI', Arial;
                font-weight: bold;
                padding: 12px 24px;
                background: rgba(0, 229, 255, 0.1);
                border: 2px solid {COLORS['border']};
                border-radius: 25px;
                min-height: 20px;
            }}
        """)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Enhanced microphone button with modern styling
        mic_container = QWidget()
        mic_layout = QVBoxLayout(mic_container)
        mic_layout.setSpacing(15)
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(120, 120)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                border: 3px solid {COLORS['border']};
                border-radius: 60px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 229, 255, 0.1), 
                    stop:1 rgba(0, 145, 234, 0.1));
                padding: 15px;
            }}
            QLabel:hover {{
                border: 3px solid rgba(0, 229, 255, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 229, 255, 0.2), 
                    stop:1 rgba(0, 145, 234, 0.2));
            }}
        """)
        
        # Initialize mic state
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        
        # Add widgets to layouts
        central_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        central_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        mic_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        central_layout.addWidget(mic_container, alignment=Qt.AlignCenter)
        
        content_layout.addStretch()
        content_layout.addWidget(central_container, alignment=Qt.AlignCenter)
        content_layout.addStretch()
        
        # Configure main widget
        self.setLayout(content_layout)
        self.setFixedSize(screen_width, screen_height)
        self.setStyleSheet(f"""
            InitialScreen {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['primary_bg']}, 
                    stop:0.4 {COLORS['secondary_bg']}, 
                    stop:1 {COLORS['accent_bg']});
            }}
        """)
        
        # Setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)        
    
    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages.strip():  # Only update if there's actual content
                    self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=80, height=80):
        try:
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
        except:
            pass

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 80, 80)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 80, 80)
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            MessageScreen {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['primary_bg']}, 
                    stop:0.3 {COLORS['secondary_bg']}, 
                    stop:1 {COLORS['accent_bg']});
            }}
        """)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):

    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(10)
        
        # Title with modern styling
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['primary_text']};
                font-size: 20px;
                font-family: 'Segoe UI', Arial;
                font-weight: bold;
                padding: 8px 16px;
            }}
        """)
        
        # Enhanced navigation buttons
        home_button = QPushButton("🏠 Home")
        home_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 229, 255, 0.2), 
                    stop:1 rgba(0, 145, 234, 0.2));
                border: 2px solid {COLORS['border']};
                border-radius: 20px;
                color: {COLORS['white_text']};
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 229, 255, 0.4), 
                    stop:1 rgba(0, 145, 234, 0.4));
                border: 2px solid rgba(0, 229, 255, 0.8);
            }}
            QPushButton:pressed {{
                background: rgba(0, 229, 255, 0.6);
            }}
        """)
        
        message_button = QPushButton("💬 Chat")
        message_button.setStyleSheet(home_button.styleSheet())
        
        # Window control buttons with modern design
        button_style = f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                color: {COLORS['white_text']};
                font-size: 12px;
                font-weight: bold;
                padding: 6px;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.3);
            }}
        """
        
        minimize_button = QPushButton("−")
        minimize_button.setStyleSheet(button_style)
        minimize_button.clicked.connect(self.minimizeWindow)
        
        self.maximize_button = QPushButton("□")
        self.maximize_button.setStyleSheet(button_style)
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        close_button = QPushButton("×")
        close_button.setStyleSheet(button_style.replace("rgba(255, 255, 255, 0.1)", "rgba(244, 67, 54, 0.3)"))
        close_button.clicked.connect(self.closeWindow)
        
        # Connect navigation
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Layout assembly
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch()
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        
        # Dragging functionality
        self.draggable = True
        self.offset = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS['secondary_bg']))
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent().showMaximized()
            self.maximize_button.setText("⧉")
            
    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
        
    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet(f"""
            MainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['primary_bg']}, 
                    stop:0.5 {COLORS['secondary_bg']}, 
                    stop:1 {COLORS['accent_bg']});
            }}
        """)
        
        top_bar = CustomTopBar(self, stacked_widget)
        top_bar.setStyleSheet(f"""
            CustomTopBar {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['secondary_bg']}, 
                    stop:1 {COLORS['accent_bg']});
                border-bottom: 2px solid {COLORS['border']};
            }}
        """)
        
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()