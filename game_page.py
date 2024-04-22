import os
import random
from PyQt6 import QtWidgets, QtCore, QtGui

class GamePage(QtWidgets.QMainWindow):
    def __init__(self, start_page, player_symbol):
        super().__init__()

        self.start_page = start_page
        self.setWindowTitle("Tic-Tac-Toe AI")
        self.setGeometry(100, 100, 500, 600)  

        self.board = ['' for _ in range(9)]
        self.player_symbol = player_symbol
        self.computer_symbol = 'O' if player_symbol == 'X' else 'X'
        self.current_player = self.player_symbol
        self.score = 0
        self.lives = 3

        self.initUI()

    def initUI(self):
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QtWidgets.QVBoxLayout(self.main_widget)

        self.grid_layout = QtWidgets.QGridLayout()

        self.grid_layout = QtWidgets.QGridLayout(self.main_widget)
        self.main_widget.setLayout(self.grid_layout)

        self.grid_layout.setSpacing(2) 
        self.grid_layout.setContentsMargins(100, 100, 100, 100) 

        self.buttons = []
        
        for i in range(3):
            row = []
            for j in range(3):
                button = QtWidgets.QPushButton('', self)
                button.setFixedSize(100, 100)
                button.setFont(QtGui.QFont('Arial', 24))
                button.clicked.connect(self.handle_button_click)
                self.grid_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.layout.addLayout(self.grid_layout)

        self.status_label = QtWidgets.QLabel(self)
        self.status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QtGui.QFont('Arial', 16))
        self.status_label.setText(f'Giliran: {self.current_player}')
        self.layout.addWidget(self.status_label)

        self.lives_label = QtWidgets.QLabel(self)
        self.lives_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lives_label.setFont(QtGui.QFont('Arial', 14))
        self.lives_label.setText(f'Nyawa: {self.lives}')
        self.layout.addWidget(self.lives_label)

        self.score_label = QtWidgets.QLabel(self)
        self.score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QtGui.QFont('Arial', 14))
        self.score_label.setText(f'Skor: {self.score}')
        self.layout.addWidget(self.score_label)

        self.restart_button = QtWidgets.QPushButton('Restart', self)
        self.restart_button.clicked.connect(self.restart_game)
        self.layout.addWidget(self.restart_button)

        self.check_score_button = QtWidgets.QPushButton('Cek Skor Terakhir', self)
        self.check_score_button.clicked.connect(self.check_score)
        self.layout.addWidget(self.check_score_button)

        self.save_button = QtWidgets.QPushButton("Save Score", self)
        self.save_button.clicked.connect(self.save_score)
        self.grid_layout.addWidget(self.save_button)
        
        self.back_to_start_button = QtWidgets.QPushButton('Kembali ke Halaman Awal', self)
        self.back_to_start_button.clicked.connect(self.go_back_to_start)
        self.layout.addWidget(self.back_to_start_button)

    def handle_button_click(self):
        button = self.sender()

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == button:
                    index = i * 3 + j
                    break

        if self.board[index] == '':
            self.board[index] = self.current_player
            button.setText(self.current_player)

            if self.check_winner(self.current_player):
                self.score += 1
                self.status_label.setText(f'{self.current_player} menang!')
                self.score_label.setText(f'Skor: {self.score}')
                self.disable_all_buttons()
                self.save_last_score()  
                return

            if '' not in self.board:
                self.status_label.setText('Permainan seri!')
                return

            self.current_player = self.computer_symbol
            self.status_label.setText(f'Giliran: {self.current_player}')

            self.ai_move()
        else:
            self.status_label.setText('Kotak sudah diisi, pilih lagi.')

    def ai_move(self):
        empty_indices = [i for i, v in enumerate(self.board) if v == '']
        ai_index = random.choice(empty_indices)

        self.board[ai_index] = self.current_player
        row, col = ai_index // 3, ai_index % 3
        self.buttons[row][col].setText(self.current_player)

        if self.check_winner(self.current_player):
            self.status_label.setText(f'{self.current_player} menang!')
            self.disable_all_buttons()
            self.save_last_score() 
            return

        if '' not in self.board:
            self.status_label.setText('Permainan seri!')
            return

        self.current_player = self.player_symbol
        self.status_label.setText(f'Giliran: {self.current_player}')

    def save_last_score(self):
        score_file_path = os.path.join(os.path.expanduser("~"), "Documents", "tic_tac_toe_last_score.txt")
        with open(score_file_path, "w") as file:
            file.write(f"Skor Terakhir: {self.score}")

    def check_score(self):
        score_file_path = os.path.join(os.path.expanduser("~"), "Documents", "tic_tac_toe_last_score.txt")
        if os.path.exists(score_file_path):
            with open(score_file_path, "r") as file:
                last_score = file.read()
            QtWidgets.QMessageBox.information(self, "Skor Terakhir", last_score)
        else:
            QtWidgets.QMessageBox.information(self, "Skor Terakhir", "Belum ada skor terakhir.")

    def check_winner(self, player):
        for i in range(3):
            if self.board[i * 3] == player and self.board[i * 3 + 1] == player and self.board[i * 3 + 2] == player:
                return True

        for j in range(3):
            if self.board[j] == player and self.board[j + 3] == player and self.board[j + 6] == player:
                return True

        if self.board[0] == player and self.board[4] == player and self.board[8] == player:
            return True

        if self.board[2] == player and self.board[4] == player and self.board[6] == player:
            return True

        return False

    def disable_all_buttons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def restart_game(self):
        self.board = ['' for _ in range(9)]
        self.current_player = self.player_symbol
        self.status_label.setText(f'Giliran: {self.current_player}')

        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)

        self.current_player = self.player_symbol
        self.status_label.setText(f'Giliran: {self.current_player}')
        self.lives = 3
        self.lives_label.setText(f'Nyawa: {self.lives}')

    def save_score(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Score", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w') as file:
                score_text = self.score_label.text() 
                file.write(score_text)
            QtWidgets.QMessageBox.information(self, "Save Score", "Score telah disimpan.")

    def go_back_to_start(self):
        self.start_page.show()
        self.close()
