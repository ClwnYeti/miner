import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QInputDialog, QButtonGroup
from PyQt5 import QtWidgets,  Qt, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from random import choice


class GameOver(Exception):
    pass


class Win(Exception):
    pass


class PushButtonRight(QPushButton):
    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()

    def __init__(self, string):
        super().__init__(string)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
            if self.game and self.press:
                self.pole.xod(self)
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()
            if self.game:
                if not(self.press):
                    self.setIcon(QIcon('pole.png'))
                    self.setIconSize(QSize(25, 25))
                    self.press = True
                else:
                    self.setIcon(QIcon('flag.png'))
                    self.setIconSize(QSize(25, 25))
                    self.press = False


class Pole:
    def __init__(self, x, y, nx, ny, bombs):
        self.nx = nx
        self.ny = ny
        self.bombs = bombs
        self.vidplayer = []
        self.vid = []
        r = []
        self.k = set()
        for i in range(nx):
            for f in range(ny):
                r.append('')
            self.vid.append(r)
            r = []
        for i in range(nx):
            for f in range(ny):
                if self.vid[i][f] == '':
                    self.checkdesk(i, f)
        for i in range(self.bombs):
            xv, yv = self.check(x, y, nx, ny)
            self.vid[xv][yv] = 'B'
        for i in range(nx):
            for f in range(ny):
                if self.vid[i][f] == '':
                    self.checkdesk(i, f)

    def checkdesk(self, x, y):
        n = 0
        for i in range(-1, 2):
            for f in range(-1, 2):
                try:
                    if x + i == -1 or y + f == -1 or \
                            (x + i == x and y + f == y):
                        raise IndexError
                    if self.vid[x + i][y + f] == 'B':
                        n += 1
                except IndexError:
                    continue
        if n == 0:
            self.vid[x][y] = ''
        else:
            self.vid[x][y] = str(n)

    def check(self, x, y, nx, ny):
        xv = choice(range(nx))
        yv = choice(range(ny))
        while self.vid[xv][yv] == 'B' or (xv == x and yv == y):
            xv = choice(range(nx))
            yv = choice(range(ny))
        return xv, yv


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.n = 50
        self.k = set()
        self.setGeometry(50, 50, 200, 100)
        self.setWindowTitle('Сапёр')
        self.button_1 = QPushButton(self)
        self.button_1.move(20, 20)
        self.button_1.setText("Настройка")
        self.button_1.clicked.connect(self.run)
        self.b_pole = QButtonGroup(self)
        self.l_pole = QButtonGroup(self)
        self.b = []
        self.l = []
        self.button_2 = QPushButton(self)
        self.button_2.move(105, 20)
        self.button_2.setText("Restart")
        self.button_2.clicked.connect(self.restart)
        self.button_2.hide()
        for f in range(25):
            for j in range(self.n):
                exec(f'self.b{f * self.n + j} = PushButtonRight(self)')
                exec(f'self.b{f * self.n + j}.pole = self')
                exec(f'self.b{f * self.n + j}.resize(25, 25)')
                exec(f'self.b{f * self.n + j}.move({j * 25 + 20},{f * 25 + 50})')
                exec(f'self.b{f * self.n + j}.x = {j}')
                exec(f'self.b{f * self.n + j}.y = {f}')
                exec(f'self.b{f * self.n + j}.hide()')
                exec(f'self.b{f * self.n + j}.press = True')
                exec(f'self.l{f * self.n + j} = QPushButton(self)')
                exec(f'self.l{f * self.n + j}.resize(25, 25)')
                exec(f'self.l{f * self.n + j}.move({j * 25 + 20},{f * 25 + 50})')
                exec(f'self.l{f * self.n + j}.x = {j}')
                exec(f'self.l{f * self.n + j}.y = {f}')
                exec(f'self.l{f * self.n + j}.setStyleSheet'
                     f'("background-color: #DCDCDC")')
                exec(f'self.l{f * self.n + j}.hide()')
                exec(f'self.b_pole.addButton(self.b{f * self.n + j})')
                exec(f'self.l_pole.addButton(self.l{f * self.n + j})')
                exec(f'self.b.append(self.b{f * self.n + j})')
                exec(f'self.l.append(self.l{f * self.n + j})')
        self.game = True
        self.b_pole.buttonClicked.connect(self.xod)
        self.l_pole.buttonClicked.connect(self.otkr)
        self.show()

    def restart(self):
        self.k = set()
        self.game = True
        for f in range(25):
            for j in range(self.n):
                self.b[f * self.n + j].game = True
                self.b[f * self.n + j].press = True
                self.l[f * self.n + j].game = True
                self.b[f * self.n + j].hide()
                self.b[f * self.n + j].setIcon(QIcon('pole.png'))
                self.b[f * self.n + j].setIconSize(QSize(25, 25))
                self.b[f * self.n + j].setStyleSheet(
                    "background-color: #FFFFFF"
                )
                self.b[f * self.n + j].setText('')
                self.l[f * self.n + j].hide()
        self.isgenereted = True
        for f in range(25):
            for j in range(self.n):
                if j < self.nx and f < self.ny:
                    self.b[f * self.n + j].show()
                else:
                    self.b[f * self.n + j].hide()
                if self.nx > 6:
                    self.button_2.move(self.nx * 25 - 55, 20)
                    self.setGeometry(50, 50, self.nx * 25 + 40,
                                     self.ny * 25 + 100)
                else:
                    self.button_2.move(105, 20)
                    self.setGeometry(50, 50, 200, self.ny * 25 + 100)

    def run(self):
        self.button_2.show()
        i, okBtnPressed = QInputDialog.getText(
            self, 'Настройка',
            "Введите через пробел: Длину, Высоту и Кол-во бомб"
        )
        if okBtnPressed:
            self.nx = int(i.split()[0])
            self.ny = int(i.split()[1])
            self.bombs = int(i.split()[2])
            self.restart()

    def xod(self, button):
        if self.isgenereted:
            self.pole = Pole(button.x, button.y, self.nx, self.ny, self.bombs)
            for i in range(self.ny):
                for f in range(self.nx):
                    self.l[i * self.n + f].setText(self.pole.vid[f][i])
            self.isgenereted = False
        try:
            if button.text() == '' and button.game:
                if self.l[button.y * self.n + button.x].text() == 'B':
                    raise GameOver
                elif self.l[button.y * self.n + button.x].text() == '':
                    self.otkr(button)
                button.hide()
                self.l[button.y * self.n + button.x].show()
                self.win()
        except GameOver:
            self.gameover()

    def win(self):
        m = 0
        for i in range(self.ny):
            for f in range(self.nx):
                if self.l[i * self.n + f].text() != 'B' and \
                        self.b[i * self.n + f].isHidden():
                    m += 1
        if m == self.nx * self.ny - self.bombs:
            for i in range(25):
                for f in range(self.n):
                    self.b[i * self.n + f].setStyleSheet(
                        "background-color: #7CFC00"
                    )
                    self.b[i * self.n + f].setIcon(QIcon('bomb.png'))
                    self.b[i * self.n + f].setIconSize(QSize(25, 25))
                    self.b[i * self.n + f].game = False


    def gameover(self):
        global bomb
        for i in range(25):
            for f in range(self.n):
                self.b[i * self.n + f].game = False
                if self.l[i * self.n + f].text() == 'B':
                    self.b[i * self.n + f].setIcon(QIcon('bomb.png'))
                    self.b[i * self.n + f].setIconSize(QSize(25, 25))

                    if self.b[i * self.n + f].press:
                        self.b[i * self.n
                               + f].setStyleSheet("background-color: #FF0000")
                    else:
                        self.b[i * self.n
                               + f].setStyleSheet("background-color: #7CFC00")
                else:
                    self.b[i * self.n
                           + f].setStyleSheet("background-color: #FF0000")
        self.game = False

    def otkr(self, button):
        self.k.add(button)
        a = set()
        if button.text() == '':
            for f in range(-1, 2):
                for i in range(-1, 2):
                    try:
                        if button.x + i == -1 or button.y + f == -1 or \
                                (button.x + i == button.x and
                                 button.y + f == button.y) \
                                or button.x + i >= self.nx or \
                                button.y + f >= self.ny:
                            raise IndexError
                        if self.l[(button.y + f) * self.n +
                                  button.x + i].text() == '':
                            a.add(self.b[(button.y + f) * self.n + button.x + i])
                        self.b[(button.y + f) * self.n + button.x + i].hide()
                        self.l[(button.y + f) * self.n + button.x + i].show()
                    except IndexError:
                        continue
            for i in a:
                if i not in self.k:
                    self.otkr(i)
        else:
            n = 0
            for f in range(-1, 2):
                for i in range(-1, 2):
                    try:
                        if (i == 0 and f == 0) or \
                                                button.x + i == -1 or \
                                                button.y + f == -1 or \
                                                button.x + i == self.nx or \
                                                button.y + f == self.ny:
                            raise IndexError
                        if not(
                               self.b[(button.y + f) * self.n +
                                      button.x + i].isHidden()
                        ) and \
                            not(
                                self.b[(button.y + f) * self.n +
                                       button.x + i].press
                                ):
                            n += 1
                        if self.l[(button.y + f) * self.n +
                                  button.x + i].text() == '':
                            a.add(self.b[(button.y + f) * self.n + button.x + i])
                    except IndexError:
                        continue
            if n >= int(self.l[button.y * self.n + button.x].text()):
                for f in range(-1, 2):
                    for i in range(-1, 2):
                        try:
                            if (i == 0 and f == 0) or button.x + i == -1 or \
                                                    button.y + f == -1 or \
                                                    button.x + i == self.nx or\
                                                    button.y + f == self.ny:
                                raise IndexError
                        except IndexError:
                            continue
                        if self.b[(button.y + f) * self.n + button.x + i].press:
                            if self.l[(button.y + f) * self.n +
                                      button.x + i].text() == 'B':
                                self.gameover()
                            else:
                                self.b[(button.y + f) * self.n + button.x + i].hide()
                                self.l[(button.y + f) * self.n + button.x + i].show()
            self.win()
            for i in a:
                if i not in self.k:
                    self.otkr(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())