import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidgetItem

from random import choice


class GameOver(Exception):
    pass


class Win(Exception):
    pass


class Pole:
    def __init__(self, razmer, bombs, x, y):
        self.b = set()
        self.razmer = razmer
        self.bombs = bombs
        self.vidplayer = []
        r = []
        for i in range(razmer):
            for f in range(razmer):
                r.append('')
            self.vidplayer.append(r)
            r = []
        self.vidplayer[x][y] = ''
        self.vid = []
        r = []
        for i in range(razmer):
            for f in range(razmer):
                r.append('')
            self.vid.append(r)
            r = []
        for i in range(bombs):
            xv, yv = self.check(x, y, razmer)
            self.vid[xv][yv] = 'B'
        for i in range(razmer):
            for f in range(razmer):
                if self.vid[i][f] == '':
                    self.checkdesk(i, f)
        self.otkr(x, y)

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
            self.vid[x][y] = '   '
        else:
            self.vid[x][y] = ' ' + str(n) + ' '

    def check(self, x, y, razmer):
        xv = choice(range(razmer))
        yv = choice(range(razmer))
        while ([y, y - 1, y + 1].count(yv) != 0
               and [x, x - 1, x + 1].count(xv) != 0) \
                or self.vid[xv][yv] == 'B':
            xv = choice(range(razmer))
            yv = choice(range(razmer))
        return xv, yv

    def xod(self, x, y, razmer, bombs):
            if self.vid[x][y] == ' B ':
                raise GameOver
            else:
                self.vidplayer[x][y] = self.vid[x][y]
                if self.vid[x][y] == '   ':
                    self.otkr(x, y)

    def otkr(self, x, y):
        self.b.add((x, y))
        a = set()
        for i in range(-1, 2):
            for f in range(-1, 2):
                try:
                    if x + i == -1 or y + f == -1 or (x + i == x and y + f == y):
                        raise IndexError
                    if self.vid[x + i][y + f] == '   ':
                        a.add((x + i, y + f))
                    self.vidplayer[x + i][y + f] = self.vid[x + i][y + f]
                except IndexError:
                    continue
        for i in a:
            if (i[0], i[1]) not in self.b:
                self.otkr(i[0], i[1])

class KnopkaLabel():
    def init(self, nx, ny):
        exec(f'self.b{nx}_{ny} = QPushButton()')
        exec(f'self.b{nx}_{ny}.resize(25, 25)')
        exec(f'self.b{nx}_{ny}.move({nx * 25 + 10},{ny * 25 + 10}')
        exec(f'self.l{nx}_{ny} = QLable()')
        exec(f'self.l{nx}_{ny}.resize(20, 20)')
        exec(f'self.l{nx}_{ny}.move({nx * 25 + 12.5},{ny * 25 + 12.5}')
        exec(f'self.l{nx}_{ny}.hide()')







class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())