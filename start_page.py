from PyQt6 import QtWidgets, QtGui, QtCore 
from game_page import GamePage

class StartPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tic-Tac-Toe AI")
        self.setGeometry(100, 100, 800, 600)  

        self.initUI()

    def initUI(self):
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("background: transparent;")

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        self.title_label = QtWidgets.QLabel("Tic Tac Toe Game", self)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.main_layout.addWidget(self.title_label)

        self.pixmap = QtGui.QPixmap("../TicTacToe_Game/assets/ai_tictac_trans.png")  

        if self.pixmap.isNull():
            print("Gagal memuat gambar.")
        else:
            self.image_label = QtWidgets.QLabel(self)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.setFixedSize(300, 300)  
            self.image_label.setScaledContents(True)
            self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            self.main_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.symbol_label = QtWidgets.QLabel("Pilih simbol Anda (X atau O):", self)
        self.main_layout.addWidget(self.symbol_label)

        self.symbol_combo = QtWidgets.QComboBox(self)
        self.symbol_combo.addItem("X")
        self.symbol_combo.addItem("O")

        self.symbol_combo.setStyleSheet("background-color: white; color: black;")

        self.main_layout.addWidget(self.symbol_combo)

        self.start_button = QtWidgets.QPushButton("Mulai Permainan", self)
        self.start_button.clicked.connect(self.start_game)
        self.main_layout.addWidget(self.start_button)

        self.quit_button = QtWidgets.QPushButton("Keluar", self)
        self.quit_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.quit_button)

    
    def start_game(self):
        player_symbol = self.symbol_combo.currentText()
        self.game_page = GamePage(self, player_symbol)
        self.game_page.show()
        self.hide()
