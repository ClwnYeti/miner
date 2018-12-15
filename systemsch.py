import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QInputDialog, QButtonGroup
from random import choice


class GameOver(Exception):
    pass


class Win(Exception):
    pass


class Pole:
    def __init__(self, x, y, nx, ny, bombs):
        self.b = set()
        self.nx = nx
        self.ny = ny
        self.bombs = bombs
        self.vidplayer = []
        self.vid = []
        r = []
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
                    if x + i == -1 or y + f == -1 or (x + i == x and y + f == y):
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

class KnopkaLabel():
    def init(self, nx, ny):
        exec(f'self.b{nx}_{ny} = QPushButton()')
        exec(f'self.b{nx}_{ny}.resize(25, 25)')
        exec(f'self.b{nx}_{ny}.move({nx * 25 + 10},{ny * 25 + 10}')
        exec(f'self.l{nx}_{ny} = QLabel()')
        exec(f'self.l{nx}_{ny}.resize(20, 20)')
        exec(f'self.l{nx}_{ny}.move({nx * 25 + 12.5},{ny * 25 + 12.5}')
        exec(f'self.l{nx}_{ny}.hide()')







class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 200, 100)
        self.setWindowTitle('Диалоговые окна')
        self.button_1 = QPushButton(self)
        self.button_1.move(20, 20)
        self.button_1.setText("Настройка")
        self.button_1.clicked.connect(self.run)
        self.b_pole = QButtonGroup(self)
        for f in range(25):
            for j in range(25):
                exec(f'self.b{j}_{f} = QPushButton(self)')
                exec(f'self.b{j}_{f}.resize(25, 25)')
                exec(f'self.b{j}_{f}.move({j * 25 + 20},{f * 25 + 50})')
                exec(f'self.b{j}_{f}.x = {j}')
                exec(f'self.b{j}_{f}.y = {f}')
                exec(f'self.b{j}_{f}.hide()')
                exec(f'self.l{j}_{f} = QLabel(self)')
                exec(f'self.l{j}_{f}.resize(20, 20)')
                exec(f'self.l{j}_{f}.move({j * 25 + 22.5},{f * 25 + 52.5})')
                exec(f'self.l{j}_{f}.hide()')
                exec(f'self.b_pole.addButton(self.b{j}_{f})')
        self.b_pole.buttonClicked.connect(self.xod)

        self.show()

    def run(self):
        i, okBtnPressed = QInputDialog.getText(
            self, 'Настройка', "Введите через пробел: Длину, Высоту и Кол-во бомб"
        )
        if okBtnPressed:
            self.nx = int(i.split()[0])
            self.ny = int(i.split()[1])
            self.bombs = int(i.split()[2])
            self.isgenereted = True
            for f in range(25):
                for j in range(25):
                    if j < self.nx and f < self.ny:
                        exec(f'self.b{j}_{f}.show()')
                    else:
                        exec(f'self.b{j}_{f}.hide()')
                    if self.nx > 6:
                        self.setGeometry(50, 50, self.nx * 25 + 40, self.ny * 25 + 100)
                    else:
                        self.setGeometry(50, 50, 200, self.ny * 25 + 100)

    def xod(self, button):
        if self.isgenereted:
            self.pole = Pole(button.x, button.y, self.nx, self.ny, self.bombs)
            for i in range(self.ny):
                for f in range(self.nx):
                    exec(f'self.l{f}_{i}.setText(self.pole.vid[{f}][{i}])')
            self.isgenereted = False
        button.hide()
        exec(f'self.l{button.x}_{button.y}.show()')







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())