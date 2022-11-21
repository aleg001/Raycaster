"""
Proyecto Raycasting
Realizado por: Alejandro Gomez


Incisos realizados:
* (0 a 30 puntos) Según la estética de su nivel  ✅
* (0 a 30 puntos) Según cuantos fps pueda renderizar su software  ✅
    * 10 puntos mas por colocar un contador de fps ✅
* (20 puntos) Por implementar una cámara con movimiento hacia delante y hacia atrás y rotación (como la que hicimos en clase)  ✅
    * No debe poder atravesar a las paredes ✅
* (10 puntos) Por implementar un minimapa que muestre la posición de jugador en el mundo. ✅
* (5 puntos) Por agregar música de fondo.  ✅
    * (??? puntos) Haber hecho y grabado el arreglo de la canción del Nivel 1.  ✅
* (10 puntos) Por agregar efectos de sonido  ✅
* (20 puntos) Por agregar al menos 1 animación a alguna sprite en la pantalla  ✅
* ??? puntos Por agregar otro sprite animado a alguna sprite en la pantalla  ✅
* (5 puntos) Por agregar una pantalla de bienvenida ✅
    * (10 puntos mas) si la pantalla permite seleccionar entre multiples niveles ✅
* (10 puntos) Por agregar una pantalla de exito cuando se cumpla una condicion en el nivel  ✅


TOTAL: ¡Muchos puntos!

"""


# Imports necesarios
import math
import time
import pygame as glfw
from OpenGL.GL import *
from pygame.locals import *
from math import *
from pygame import mixer

# Definicion de constantes de colores
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
GREEN = (45, 96, 29)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SKYBLUE = (135, 206, 235)
GREY = (128, 128, 128)
DARKGREY = (40, 40, 40)

# Paredes cargadas
walls = {
    "1": glfw.image.load("Texturas/pared.png"),
    "2": glfw.image.load("Texturas/paredB.png"),
    "3": glfw.image.load("Texturas/Suelo.png"),
    "4": glfw.image.load("Texturas/metal.png"),
    "5": glfw.image.load("Texturas/floor4.png"),
    "6": glfw.image.load("Texturas/danger6.png"),
}

# Elementos cargados
assets = {
    "1": glfw.image.load("Texturas/bg.jpeg"),
    "2": glfw.image.load("Texturas/grass1.png"),
    "3": glfw.image.load("Texturas/chemicalPlant.png"),
}


# Refrencia animacion:
# https://www.geeksforgeeks.org/pygame-character-animation/
rings = [
    # Scale image: https://www.geeksforgeeks.org/how-to-rotate-and-scale-images-using-pygame/
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring1.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring2.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring3.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring4.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring5.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring6.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring7.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring8.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring9.png"), (30, 30)),
    glfw.transform.scale(glfw.image.load("Sprites/rings/ring10.png"), (30, 30)),
]

sonic = [
    # Scale image: https://www.geeksforgeeks.org/how-to-rotate-and-scale-images-using-pygame/
    glfw.transform.scale(glfw.image.load("Sprites/sonic/sonic1.png"), (55, 55)),
    glfw.transform.scale(glfw.image.load("Sprites/sonic/sonic2.png"), (55, 55)),
    glfw.transform.scale(glfw.image.load("Sprites/sonic/sonic3.png"), (55, 55)),
    glfw.transform.scale(glfw.image.load("Sprites/sonic/sonic4.png"), (55, 55)),
]

"""
Inspirado en ejemplos brindados
en clase del gran profe DENNIS ALDANA
"""


class Raycaster(object):
    def __init__(self, screen) -> None:
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.blockSize = 50
        self.map = []
        self.player = {
            "x": int(self.blockSize + self.blockSize / 2),
            "y": int(self.blockSize + self.blockSize / 2),
            "FieldOfView": int(pi / 3),
            "Angle": int(pi / 3),
        }

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.blockSize):
            for j in range(y, y + self.blockSize):
                tx = int((i - x) * 128 / self.blockSize)
                ty = int((j - y) * 128 / self.blockSize)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def loadmap(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self, x, h, c, tx):
        start_y = int(self.height / 2 - h / 2)
        end_y = int(self.height / 2 + h / 2)
        height = end_y - start_y

        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)

    def drawMap(self):
        var1 = int(self.blockSize)
        for x in range(0, 500, var1):
            for y in range(0, 500, var1):
                i = x / self.blockSize
                j = y / self.blockSize
                i = int(i)
                j = int(j)
                if self.map[j][i] != " ":
                    self.block(x, y, walls[self.map[j][i]])

    def drawPlayer(self):
        self.point(self.player.get("x"), self.player.get("y"))

    def draw(self):
        self.drawMap()
        self.drawPlayer()
        density = 100

        for i in range(0, density):
            a = (
                self.player["Angle"]
                - self.player["FieldOfView"] / 2
                + self.player["FieldOfView"] * i / density
            )
            d, c, _ = self.castRay(a)

        for i in range(0, int(self.width / 2)):

            try:
                a = (
                    self.player["Angle"]
                    - self.player["FieldOfView"] / 2
                    + self.player["FieldOfView"] * i / (self.width / 2)
                )
                d, c, tx = self.castRay(a)

                x = int(self.width / 2) + i

                h = self.height / (d * cos(a - self.player["Angle"])) * self.height / 10

                self.draw_stake(x, h, c, tx)

            # Verificacion en caso toque una pared para evitar que se rompa programa
            except:
                self.player["x"] = int(
                    self.blockSize + self.blockSize / (cos(a - self.player["Angle"]))
                )
                self.player["y"] = int(
                    +self.blockSize / (cos(a - self.player["Angle"]))
                )

    def draw_sprite(self, sprite):
        spriteX = 500
        spriteY = 0
        spriteSize = 128
        for x in range(spriteX, spriteX + spriteSize):
            for y in range(spriteY, spriteY + spriteSize):
                tx = int((x - spriteX) * 128 / spriteSize)
                ty = int((y - spriteY) * 128 / spriteSize)
                c = sprite["sprite"].get_at((tx, ty))
                if x > 500:
                    self.point(x, y, c)

    def castRay(self, a):
        d = 0
        ox = self.player["x"]
        oy = self.player["y"]

        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / self.blockSize)
            j = int(y / self.blockSize)

            if self.map[j][i] != " ":
                hitx = x - i * self.blockSize
                hity = y - j * self.blockSize

                if 1 < hitx < self.blockSize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blockSize)
                return d, self.map[j][i], tx

            self.point(x, y, CYAN)
            self.screen.set_at((x, y), CYAN)

            d += 1


# Incializacion de pygame
glfw.init()
glfw.mouse.set_visible(True)
screen = glfw.display.set_mode((1000, 500), glfw.DOUBLEBUF | glfw.HWACCEL)
screen.set_alpha(None)
background = glfw.image.load("Texturas/menu.jpeg")


# Se crean los botones como clase

"""
Se tomo como referencia el siguiente video:
https://www.youtube.com/watch?v=GMBqjxcKogA&ab_channel=BaralTech

Cabe destacar que se adaptó para las necesidades de este proyecto
"""


class BotonesMenu:
    def __init__(self, image, position, textoInput, fuente, color, colorSeleccionado):
        self.image = image
        self.xPos = position[0]
        self.yPos = position[1]
        self.fuente = fuente
        self.color, self.colorSeleccionado = color, colorSeleccionado
        self.textoInput = textoInput
        self.text = self.fuente.render(self.textoInput, True, self.color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))
        self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))

    def actualizarMenu(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    def VerInput(self, posicion):
        if posicion[0] in range(self.rect.left, self.rect.right) and posicion[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.fuente.render(
                self.textoInput, True, self.colorSeleccionado
            )
            return True
        return False

    def CambiarColores(self, posicion):
        if posicion[0] in range(self.rect.left, self.rect.right) and posicion[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.fuente.render(
                self.textoInput, True, self.colorSeleccionado
            )
        else:
            self.text = self.fuente.render(self.textoInput, True, self.color)


r = Raycaster(screen)

running = True
# Mejorar frames
# Referencia: https://www.codeproject.com/Articles/5298051/Improving-Performance-in-glfw-Speed-Up-Your-Game
walls.get("1").convert()
walls.get("2").convert()
walls.get("3").convert()
walls.get("4").convert()
walls.get("5").convert()
walls.get("6").convert()

Clock1 = glfw.time.Clock()

"""
Funcion realizada para
el renderizado de los 2 niveles
disponibles en el juego.

Cada nivel esta inspirado en una zona icónica de Sonic

1. Green Hill Zone de Sonic 1
2. Chemical Plant Zone de Sonic 2
"""


def Niveles(Nivel):

    glfw.mouse.set_visible(False)
    # Mapa segun el nivel
    if Nivel == 1:
        r.loadmap("map.txt")
    if Nivel == 2:
        r.loadmap("map2.txt")
    val = 0
    val2 = 0

    # Musica segun el nivel
    mixer.init()
    if Nivel == 1:
        mixer.music.load("Sounds/Sonic.mp3")

    if Nivel == 2:
        mixer.music.load("Sounds/chemical.mp3")
    mixer.music.play(-1)

    while True:

        # Se carga Green Hill Zone
        if Nivel == 1:
            screen.fill(GREEN)
            screen.blit(assets["1"], (r.width / 2, 0, r.width, r.height / 2))
            screen.fill(GREEN, (r.width / 2, r.height / 2, r.width, r.height / 2))

        # Se carga Chemical Plant Zone
        if Nivel == 2:
            screen.fill(DARKGREY)
            screen.blit(assets["3"], (r.width / 2, 0, r.width, r.height / 2))
            screen.fill(DARKGREY, (r.width / 2, r.height / 2, r.width, r.height / 2))

        r.draw()
        Clock1.tick(60) / 1000.0

        if val >= len(rings):
            val = 0

        if val2 >= len(sonic):
            val2 = 0

        # Gif de anillos
        im = rings[val]
        # Gif de Sonic
        sonicSprite = sonic[val2]

        screen.blit(sonicSprite, (r.player["x"], r.player["y"]))
        posMini = (r.player["x"] - 8, r.player["y"] - 8)

        if Nivel == 1:
            screen.blit(im, (400, 300))
            # Se realiza un rango en el cual se considera victoria
            if 340 <= posMini[0] <= 440 and 250 <= posMini[1] <= 340:
                mixer.Sound("Sounds/mario.mp3").play()
                # Se lanza a pantalla de victoria
                Victoria()
        if Nivel == 2:
            screen.blit(im, (400, 400))
            # Se realiza un rango en el cual se considera victoria
            if 340 <= posMini[0] <= 440 and 350 <= posMini[1] <= 440:
                mixer.Sound("Sounds/mario.mp3").play()
                # Se lanza a pantalla de victoria
                Victoria()

        glfw.display.update()

        Clock1.tick(15 * 2)

        val += 1
        val2 += 1

        for event in glfw.event.get():
            if event.type == glfw.QUIT or (
                event.type == glfw.KEYDOWN and event.key == glfw.K_ESCAPE
            ):
                # Efectos de sonido
                mixer.quit()
                mixer.init()
                mixer.Sound("Sounds/bye.mp3").play()
                time.sleep(3)
                exit(0)

            if event.type == glfw.KEYDOWN:

                if event.key == glfw.K_RIGHT:
                    r.player["Angle"] += pi / 10

                elif event.key == glfw.K_LEFT:
                    r.player["Angle"] -= pi / 10

                elif event.key == glfw.K_w:
                    r.player["y"] += 15
                    # Efectos de sonido
                    mixer.Sound("Sounds/walk.mp3").play()

                elif event.key == glfw.K_s:
                    r.player["y"] -= 15
                    # Efectos de sonido
                    mixer.Sound("Sounds/walk.mp3").play()

                elif event.key == glfw.K_a:
                    r.player["x"] -= 15
                    # Efectos de sonido
                    mixer.Sound("Sounds/walk.mp3").play()

                elif event.key == glfw.K_d:
                    r.player["x"] += 15
                    # Efectos de sonido
                    mixer.Sound("Sounds/walk.mp3").play()

                # 15 frames
                Clock1.tick(15)
                glfw.display.set_caption(
                    "Sonic Raycaster - FPS: {}".format(math.ceil(Clock1.get_fps()))
                )

                glfw.display.update()


"""
Funcion realizada para renderizar
pantalla del menu principal
"""


def MenuPrincipal():
    glfw.display.set_caption("Sonic Raycaster")
    mixer.init()
    mixer.music.load("Sounds/menuMusic.mp3")
    mixer.music.play(-1)
    while True:
        screen.blit(background, (0, 0))

        PosicionMouseMenu = glfw.mouse.get_pos()

        textoMostrarMenu = glfw.font.SysFont("Amarillo", 90).render(
            "Sonic Raycaster", True, "#3061E3"
        )
        fondoOpcionesMenu = textoMostrarMenu.get_rect(center=(500, 100))

        JugarNivel1 = BotonesMenu(
            image=glfw.image.load("Texturas/recta.png"),
            position=(500, 200),
            textoInput="Jugar nivel 1 (GHZ)",
            fuente=glfw.font.SysFont("Times New Roman", 30),
            color="#d7fcd4",
            colorSeleccionado="Blue",
        )

        JugarNivel2 = BotonesMenu(
            image=glfw.image.load("Texturas/recta.png"),
            position=(500, 300),
            textoInput="Jugar nivel 2 (CPZ)",
            fuente=glfw.font.SysFont("Times New Roman", 30),
            color="#d7fcd4",
            colorSeleccionado="Blue",
        )

        salirJuego = BotonesMenu(
            image=glfw.image.load("Texturas/recta.png"),
            position=(500, 400),
            textoInput="Salir",
            fuente=glfw.font.SysFont("Times New Roman", 30),
            color="#d7fcd4",
            colorSeleccionado="Red",
        )

        screen.blit(textoMostrarMenu, fondoOpcionesMenu)

        for button in [JugarNivel1, JugarNivel2, salirJuego]:
            button.CambiarColores(PosicionMouseMenu)
            button.actualizarMenu(screen)

        for event in glfw.event.get():
            if event.type == glfw.QUIT or (
                event.type == glfw.KEYDOWN and event.key == glfw.K_ESCAPE
            ):
                # Efectos de sonido
                mixer.quit()
                mixer.init()
                mixer.Sound("Sounds/bye.mp3").play()
                time.sleep(3)
                exit(0)
            if event.type == glfw.MOUSEBUTTONDOWN:
                if JugarNivel1.VerInput(PosicionMouseMenu):
                    mixer.Sound("Sounds/menuOption.mp3").play()
                    time.sleep(3)
                    Niveles(1)

                if JugarNivel2.VerInput(PosicionMouseMenu):
                    mixer.Sound("Sounds/menuOption.mp3").play()
                    time.sleep(3)
                    Niveles(2)
                if salirJuego.VerInput(PosicionMouseMenu):
                    mixer.Sound("Sounds/menuOption.mp3").play()
                    mixer.quit()
                    mixer.init()
                    mixer.Sound("Sounds/bye.mp3").play()
                    time.sleep(3)
                    glfw.quit()
                    exit(0)

        glfw.display.update()


"""
Funcion realizada para renderizar
pantalla de victoria
"""


def Victoria():
    mixer.init()
    mixer.music.load("Sounds/victory.mp3")
    mixer.music.play(-1)
    while True:
        glfw.mouse.set_visible(True)
        screen.blit(background, (0, 0))
        PosicionMouseMenu = glfw.mouse.get_pos()

        textoMostrarMenu = glfw.font.SysFont("Amarillo", 90).render(
            "¡Felicidades!", True, "#3061E3"
        )
        fondoOpcionesMenu = textoMostrarMenu.get_rect(center=(500, 100))

        salirJuego = BotonesMenu(
            image=glfw.image.load("Texturas/recta.png"),
            position=(500, 400),
            textoInput="Salir",
            fuente=glfw.font.SysFont("Times New Roman", 30),
            color="#d7fcd4",
            colorSeleccionado="Red",
        )

        screen.blit(textoMostrarMenu, fondoOpcionesMenu)

        for button in [salirJuego]:
            button.CambiarColores(PosicionMouseMenu)
            button.actualizarMenu(screen)

        for event in glfw.event.get():
            if event.type == glfw.QUIT or (
                event.type == glfw.KEYDOWN and event.key == glfw.K_ESCAPE
            ):
                # Efectos de sonido
                mixer.quit()
                mixer.init()
                mixer.Sound("Sounds/bye.mp3").play()
                time.sleep(3)
                exit(0)
            if event.type == glfw.MOUSEBUTTONDOWN:
                if salirJuego.VerInput(PosicionMouseMenu):
                    mixer.Sound("Sounds/menuOption.mp3").play()
                    mixer.quit()
                    mixer.init()
                    mixer.Sound("Sounds/bye.mp3").play()
                    time.sleep(3)
                    glfw.quit()
                    exit(0)

        glfw.display.update()


# Se llama a la pantalla principal
MenuPrincipal()
