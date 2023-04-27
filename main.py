import pygame
import math as m
from PIL import Image as img
import numpy as np

SCR_WIDTH = 600
SCR_HEIGHT = 600


def set_pixel(p, cor):
    xi, yi = p
    if 0 < yi <= SCR_HEIGHT and SCR_WIDTH > xi >= 0:
        screen.set_at((xi, SCR_HEIGHT - yi), cor)


def read_pixel(p):
    xi, yi = p
    cor = (-1, -1, -1, -1)
    if 0 < yi <= SCR_HEIGHT and SCR_WIDTH > xi >= 0:
        cor = screen.get_at((xi, SCR_HEIGHT - yi))
    return cor


class Pilha:
    pilha = []

    def empilhar(self, elemx, elemy):
        elem = (elemx, elemy)
        self.pilha.append(elem)

    def desempilhar(self):
        elem = self.pilha.pop()
        return elem


class Poligono:
    def __init__(self):
        self.pontos = []
        self.cores = []

    def add(self, p1, p2, cor = None):
        if cor is None:
            x1, y1 = p1
            s1, t1 = p2
            self.pontos.append((x1, y1))
            self.cores.append((s1, t1))
        else:
            self.pontos.append((p1, p2))
            self.cores.append(cor)


    def desenha(self, cor):
        for ponto in range(len(self.pontos)):
            xi, yi = self.pontos[ponto]
            if ponto == len(self.pontos) - 1:
                xf, yf = self.pontos[0]
            else:
                xf, yf = self.pontos[ponto+1]
            bresenham(xi, yi, xf, yf, cor)


def dda(x1, y1, x2, y2, cor1, cor2):
    set_pixel((x2, y2), cor2)
    dx = x2-x1
    dy = y2-y1
    if abs(dx) > abs(dy):
        passos = abs(dx)
    else:
        passos = abs(dy)

    if passos == 0:
        set_pixel((x1, y1), cor1)
        return

    passox = dx/passos
    passoy = dy/passos

    for elem in range(m.trunc(passos)):
        xf = round(x1 + elem*passox)
        yf = round(y1 + elem*passoy)
        r1, g1, b1, a1 = cor1
        r1 = ((passos-elem)/passos) * r1
        g1 = ((passos-elem) / passos) * g1
        b1 = ((passos-elem) / passos) * b1
        r2, g2, b2, a2 = cor2
        r2 = (elem / passos) * r2
        g2 = (elem / passos) * g2
        b2 = (elem / passos) * b2
        cor = (round(r1 + r2), round(g1 + g2), round(b1 + b2), 255)
        set_pixel((xf, yf), cor)


def bresenham(x1, y1, x2, y2, cor):
    dx = x2 - x1
    dy = y2 - y1

    xf = x1
    yf = y1

    if dx < 0:
        factorx = -1
    else:
        factorx = 1

    if dy < 0:
        factory = -1
    else:
        factory = 1

    if abs(dx) >= abs(dy):
        p = -abs(dx) + (2*abs(dy))

        for i in range(round(abs(dx))):
            set_pixel((round(xf), round(yf)), cor)

            xf = xf + factorx
            if p >= 0:
                yf = yf + factory
                p = p - (2*abs(dx)) + (2*abs(dy))
            else:
                p = p + (2*abs(dy))
    else:
        p = -dy + (2 * abs(dx))

        for i in range(abs(dy)):
            set_pixel((round(xf), round(yf)), cor)

            yf = yf + factory
            if p >= 0:
                xf = xf + factorx
                p = p - (2 * abs(dy)) + (2 * abs(dx))
            else:
                p = p + (2 * abs(dx))


def flood(xi, yi, fcolor):
    colori = read_pixel((xi, yi))
    if colori == fcolor:
        return
    pilha = Pilha()
    pilha.empilhar(xi, yi)
    while len(pilha.pilha) != 0:
        posicao = pilha.desempilhar()
        xn, yn = posicao
        if screen.get_at((xn+1, yn)) == colori and xn+1 < SCR_WIDTH:
            pilha.empilhar(xn+1, yn)
        if screen.get_at((xn-1, yn)) == colori and xn-1 > 0:
            pilha.empilhar(xn-1, yn)
        if screen.get_at((xn, yn+1)) == colori and yn+1 < SCR_HEIGHT:
            pilha.empilhar(xn, yn+1)
        if screen.get_at((xn, yn-1)) == colori and yn-1 > 0:
            pilha.empilhar(xn, yn-1)
        set_pixel((xn, yn), fcolor)


def intersect(scan, pi, pf):
    xi, yi = pi
    xf, yf = pf
    if yi == yf:
        return -1, -1
    if yi < yf:
        aux = yi
        yi = yf
        yf = aux
        aux = xi
        xi = xf
        xf = aux

    if (yf - yi) == 0:
        return -1, -1

    t = (scan - yf)/(yi - yf)

    if 1 >= t > 0:
        polx = xf + t*(xi - xf)
        return polx, t
    else:
        return -1, -1


def scanline(pol):
    t = 0
    for scan in range(SCR_HEIGHT):
        hey = []
        degrad = []
        for indice in range(len(pol.pontos)):
            pi = pol.pontos[indice]
            if indice == len(pol.pontos) - 1:
                pf = pol.pontos[0]
                corf = pol.cores[0]
            else:
                pf = pol.pontos[indice+1]
                corf = pol.cores[indice+1]
            polx, t = intersect(scan, pi, pf)
            if polx != -1:
                xi, yi = pi
                xf, yf = pf
                if yi < yf:
                    degrad.append((corf, pol.cores[indice], t))
                else:
                    degrad.append((pol.cores[indice], corf, t))
                hey.append((polx, scan))
                for elem in range(len(hey)-1, 0, -1):
                    difx0, scan = hey[elem]
                    difx1, scan = hey[elem-1]
                    difcori0, difcorf0, difactor0 = degrad[elem]
                    difcori1, difcorf1, difactor1 = degrad[elem-1]
                    if difx1 >= difx0:
                        hey[elem] = (difx1, scan)
                        degrad[elem] = (difcori1, difcorf1, difactor1)
                        hey[elem-1] = (difx0, scan)
                        degrad[elem-1] = (difcori0, difcorf0, difactor0)
        for linha in range(0, len(hey), 2):
            cor1, cor2, t = degrad[linha]
            r1, g1, b1, a1 = cor1
            r2, g2, b2, a2 = cor2
            r = r1*t + r2*(1-t)
            g = g1*t + g2*(1-t)
            b = b1*t + b2*(1-t)
            cori = (r, g, b, a1)
            cor1, cor2, t = degrad[linha+1]
            r1, g1, b1, a1 = cor1
            r2, g2, b2, a2 = cor2
            r = r1 * t + r2 * (1 - t)
            g = g1 * t + g2 * (1 - t)
            b = b1 * t + b2 * (1 - t)
            corf = (r, g, b, a1)
            xi, yi = hey[linha]
            xf, yf = hey[linha+1]
            dda(round(xi), round(yi), round(xf), round(yf), cori, corf)


def loadimg(path):
    image = img.open(path)
    image = image.convert("RGB")
    mat = np.asarray(image)
    return mat


def dda_tex(x1, y1, x2, y2, tex1, tex2, mat):
    lin, col, ch = mat.shape
    s2, t2 = tex2
    s1, t1 = tex1

    set_pixel((x2, y2), mat[round((lin-1)*(1-t2)), round(s2*(col-1))])
    dx = x2-x1
    dy = y2-y1
    if abs(dx) > abs(dy):
        passos = abs(dx)
    else:
        passos = abs(dy)

    if passos == 0:
        set_pixel((x1, y1), mat[round((lin-1)*(1-t1)), round(s1*(col-1))])
        return

    passox = dx/passos
    passoy = dy/passos

    for elem in range(m.trunc(passos)):
        xf = round(x1 + elem*passox)
        yf = round(y1 + elem*passoy)
        ds = abs(s1 - s2)/passos
        dt = abs(t1 - t2)/passos
        si = min(s1, s2)
        ti = min(t1, t2)
        s = (ds * elem) + si
        t = (dt * elem) + ti

        cor = mat[round((lin-1)*(1-t)), round(s * (col-1))]
        set_pixel((xf, yf), cor)


def tex_scanline(pol, mat):
    t = 0
    for scan in range(SCR_HEIGHT):
        hey = []
        degrad = []
        for indice in range(len(pol.pontos)):
            pi = pol.pontos[indice]
            if indice == len(pol.pontos) - 1:
                pf = pol.pontos[0]
                corf = pol.cores[0]
            else:
                pf = pol.pontos[indice+1]
                corf = pol.cores[indice+1]
            polx, t = intersect(scan, pi, pf)
            if polx != -1:
                xi, yi = pi
                xf, yf = pf
                if yi < yf:
                    degrad.append((corf, pol.cores[indice], t))
                else:
                    degrad.append((pol.cores[indice], corf, t))

                hey.append((polx, scan))
                for elem in range(len(hey)-1, 0, -1):
                    difx0, scan = hey[elem]
                    difx1, scan = hey[elem-1]
                    difs0, dift0, difactor0 = degrad[elem]
                    difs1, dift1, difactor1 = degrad[elem-1]
                    if difx1 >= difx0:
                        hey[elem] = (difx1, scan)
                        degrad[elem] = (difs1, dift1, difactor1)
                        hey[elem-1] = (difx0, scan)
                        degrad[elem-1] = (difs0, dift0, difactor0)
        for linha in range(0, len(hey), 2):
            xi, yi = hey[linha]
            xf, yf = hey[linha + 1]

            tex1, tex2, factor = degrad[linha]
            s1, t1 = tex1
            s2, t2 = tex2
            s = s1 * factor + s2 * (1 - factor)
            t = t1 * factor + t2 * (1 - factor)
            texi = (s, t)

            if xf > 450 and 50 < yf < 150:
                print(texi, factor)

            tex1, tex2, factor = degrad[linha+1]
            s1, t1 = tex1
            s2, t2 = tex2
            s = s1 * factor + s2 * (1 - factor)
            t = t1 * factor + t2 * (1 - factor)
            texf = (s, t)

            dda_tex(round(xi), round(yi), round(xf), round(yf), texi, texf, mat)


pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("Bananya")

textura = loadimg("gato.jpg")

colour = (0, 255, 0, 255)
azul = (0, 0, 255, 255)

figura = Poligono()
figura.add(50, 50, azul)
figura.add(50, 250, colour)
figura.add(150, 150, (0, 255/2, 255/2, 255))
figura.add(250, 250, colour)
figura.add(250, 50, azul)

figurao = Poligono()
figurao.add((350, 50), (0.0, 0.0))
figurao.add((350, 350), (0.0, 1.0))
figurao.add((550, 350), (1.0, 1.0))
figurao.add((550, 50), (1.0, 0.0))
figurao.add((450, 200), (0.5, 0.5))

opened = True

while opened:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            opened = False

    tex_scanline(figurao, textura)
    scanline(figura)

    pygame.display.update()
    for i in range(SCR_WIDTH):
        for j in range(SCR_HEIGHT):
            screen.set_at((i, j), (0, 0, 0, 0))

pygame.quit()
