import pygame
import sys
import Unit_Object
from Screen_Object import objects


unit = Unit_Object.Unit()

# --- Couleurs ---
BLANC      = (255, 255, 255)
GRIS       = (180, 180, 180)
GRIS_FONCE = (100, 100, 100)
NOIR       = (0,   0,   0)
ROUGE      = (255, 0,   0)

rodsLists = [False for _ in range(24)]
rods_state = 0


# ── Callbacks globaux ─────────────────────────────────────────────────────────

def leave(a=None):
    pygame.quit()
    sys.exit()

def barres(a):
    global rods_state
    rods_state = a

def nothing(a=None):
    pass

def antoine(a=None):
    rodsLists[a - 1] = not rodsLists[a - 1]

def changeBg(arg):
    global GLOBALplan, plan, bg
    bg = arg
    if bg not in GLOBALplan:
        GLOBALplan[bg] = objects(
            Poussoir, Afficheur, Levier, Jauge, Impulsion, HoldButton,
            antoine, unit, rodsLists, nothing, leave, barres, changeBg, bg
        )
    plan = GLOBALplan[bg]


# ── Mise à jour afficheurs barres (bg=0) ──────────────────────────────────────

def change_rod_value():
    c = 24
    for x in range(len(unit.reactor.assembly)):
        for y in range(len(unit.reactor.assembly[x])):
            if unit.reactor.assembly[x][y] is None:
                continue
            plan["rod" + str(c)].change_valeur(
                int(unit.reactor.assembly[x][y].rods_pulled)
            )
            c -= 1


# ── Mise à jour afficheurs turbine (bg=1) ─────────────────────────────────────

def update_turbine_screen():
    t   = unit.turbine
    scr = GLOBALplan.get(1)
    if scr is None:
        return
    rpm = t.get_rpm()
    #scr["turb_rpm"].change_valeur(rpm)
    #scr["turb_power"].change_valeur(t.get_power())
    scr["turb_rpm_num"].change_valeur(f"{rpm} rpm")
    scr["turb_power_num"].change_valeur(f"{t.get_power():.1f} MW")
    scr["turb_valve_num"].change_valeur(f"Valve: {t.valve:.1f}%")
    scr["turb_bypass_num"].change_valeur(f"Bypass: {t.bypass:.1f}%")
    scr["turb_pressure_num"].change_valeur(f"Press: {round(unit.reactor.pressure)}")
    if t.is_sync():
        scr["turb_sync"].change_valeur("SYNC")
        scr["turb_breaker_state"].change_valeur("ON GRID")
    else:
        ecart = abs(rpm - t.RPM_CIBLE)
        scr["turb_sync"].change_valeur(
            f"READY ({ecart:.0f})" if ecart < 50 else f"FREE ({rpm:.0f})"
        )
        scr["turb_breaker_state"].change_valeur("OFF GRID")


# ── Gestion des HoldButtons au fast_refresh ───────────────────────────────────

def process_hold_buttons():
    for obj in plan.values():
        if isinstance(obj, HoldButton) and obj.held:
            obj.func(obj.arg)


# ── Classes sprites ───────────────────────────────────────────────────────────

class Sprite:
    def __init__(self, x, y, L=40, l=20, type="img/type.png", nom="bo"):
        self.x = x; self.y = y; self.L = L; self.l = l
        self.type = type; self.nom = nom


class Poussoir(Sprite):
    """Toggle classique — reste enfoncé."""
    def __init__(self, x, y, L=50, l=50,
                 type="img/bouton_vert1.png", typeBis="img/bouton_vert2.png",
                 nom="bo", func=None, arg=None, func2=None, arg2=None,
                 on=False, verr=False, liens=None, label=""):
        super().__init__(x, y, L, l, type, nom)
        self.clicked = False
        self.on      = on
        self.typeBis = typeBis
        self.func    = func  if func  is not None else nothing
        self.arg     = arg
        self.func2   = func2 if func2 is not None else nothing
        self.arg2    = arg2
        self.liens   = liens if liens is not None else []
        self.verr    = verr
        self.label   = label

    def switch(self):
        self.on = not self.on
        self.func2(self.arg2)


class Impulsion(Sprite):
    """Momentané — revient automatiquement à off après le clic."""
    def __init__(self, x, y, L=50, l=50,
                 type="img/bouton_vert1.png", typeBis="img/bouton_vert2.png",
                 nom="bo", func=None, arg=None, label=""):
        super().__init__(x, y, L, l, type, nom)
        self.clicked = False
        self.on      = False
        self.typeBis = typeBis
        self.func    = func if func is not None else nothing
        self.arg     = arg
        self.label   = label
        self.liens = []; self.verr = False
        self.func2 = nothing; self.arg2 = None


class HoldButton(Sprite):
    """Maintenu — action répétée au fast_refresh tant que le bouton est tenu."""
    def __init__(self, x, y, L=50, l=50,
                 type="img/bouton_vert1.png", typeBis="img/bouton_vert2.png",
                 nom="bo", func=None, arg=None, label=""):
        super().__init__(x, y, L, l, type, nom)
        self.held    = False
        self.on      = False
        self.typeBis = typeBis
        self.func    = func if func is not None else nothing
        self.arg     = arg
        self.label   = label
        self.liens = []; self.verr = False
        self.func2 = nothing; self.arg2 = None; self.clicked = False


class Levier(Poussoir):
    def __init__(self, x, y, L=20, l=37,
                 type="img/levier.png", typeBis="img/levier_.png",
                 nom="bo", func=None, arg=None, func2=None, arg2=None,
                 on=False, verr=False, liens=None, label=""):
        super().__init__(x, y, L, l, type, typeBis, nom,
                         func, arg, func2, arg2, on, verr, liens, label)


class Afficheur(Sprite):
    def __init__(self, x, y, L=56, l=44, type="img/num.png", nom="bo", valeur=0):
        super().__init__(x, y, L, l, type, nom)
        self.valeur = valeur

    def change_valeur(self, v):
        self.valeur = v



class Jauge(Afficheur):
    def __init__(self,x,y,L=70,l=49,type="img/cadrant.png",nom="bo",valeur=0,MAX=10):
        Afficheur.__init__(self,x,y,L,l,type,nom,valeur)
        self.MAX=MAX
        deg = 0
        self.deg=deg
        self.box = pygame.Rect(x,y,L,l)

    def change_valeur(self,valeur):
        self.valeur = valeur
        MAX = self.MAX
        valeur = valeur%MAX
        self.deg=int(round((valeur/MAX)*180,0))


# ── Initialisation Pygame ──────────────────────────────────────────────────────

pygame.init()

VIRTUAL_W, VIRTUAL_H = 1920, 1080
real_w = pygame.display.Info().current_w
real_h = pygame.display.Info().current_h
scale  = min(real_w / VIRTUAL_W, real_h / VIRTUAL_H)

virtual_screen = pygame.Surface((VIRTUAL_W, VIRTUAL_H))
ecran = pygame.display.set_mode((real_w, real_h))
pygame.display.set_caption("Projet : VOLNA")

font       = pygame.font.SysFont(None, 36)
font_label = pygame.font.SysFont(None, 20)

bg = 0
GLOBALplan = {}
GLOBALplan[bg] = objects(
    Poussoir, Afficheur, Levier, Jauge, Impulsion, HoldButton,
    antoine, unit, rodsLists, nothing, leave, barres, changeBg, bg
)
plan = GLOBALplan[bg]

clock = pygame.time.Clock()


# ── Rendu ─────────────────────────────────────────────────────────────────────

def draw_label(obj, bx):
    if getattr(obj, 'label', ''):
        lbl = font_label.render(obj.label, True, NOIR)
        virtual_screen.blit(lbl, lbl.get_rect(centerx=bx.centerx, bottom=bx.top - 2))


def blit_sprite(obj, bx):
    active = getattr(obj, 'on', False) or getattr(obj, 'held', False)
    path   = obj.typeBis if active else obj.type
    try:
        img = pygame.image.load(path)
    except Exception:
        img = pygame.Surface((obj.L, obj.l))
        img.fill(GRIS_FONCE if active else GRIS)
    virtual_screen.blit(img, bx)


def bouton(obj, bx):
    souris = (pygame.mouse.get_pos()[0] / scale,
              pygame.mouse.get_pos()[1] / scale)
    clic = pygame.mouse.get_pressed()[0]
    blit_sprite(obj, bx)
    draw_label(obj, bx)
    if clic and bx.collidepoint(souris) and obj.clicked:
        for lien in obj.liens:
            btn = plan.get(lien)
            if btn and not obj.on and btn.on:
                btn.switch()
    if obj.on and obj.verr:
        return False
    return clic and bx.collidepoint(souris) and obj.clicked


def bouton_impulsion(obj, bx):
    souris = (pygame.mouse.get_pos()[0] / scale,
              pygame.mouse.get_pos()[1] / scale)
    clic = pygame.mouse.get_pressed()[0]
    blit_sprite(obj, bx)
    draw_label(obj, bx)
    if clic and bx.collidepoint(souris):
        obj.on = True
        if obj.clicked:
            obj.func(obj.arg)
            obj.clicked = False
    else:
        obj.on = False
        if not clic:
            obj.clicked = True


def bouton_hold(obj, bx):
    souris = (pygame.mouse.get_pos()[0] / scale,
              pygame.mouse.get_pos()[1] / scale)
    clic = pygame.mouse.get_pressed()[0]
    obj.held = clic and bx.collidepoint(souris)
    obj.on   = obj.held
    blit_sprite(obj, bx)
    draw_label(obj, bx)


def panneau(obj, bx):
    try:
        img = pygame.image.load(obj.type)
    except Exception:
        img = pygame.Surface((obj.L, obj.l))
        img.fill(GRIS)
    virtual_screen.blit(img, bx)
    if isinstance(obj, Jauge):
        try:
            aig = pygame.transform.rotate(pygame.image.load("img/aiguille.png"), -obj.deg)
        except Exception:
            aig = pygame.Surface((10, 40), pygame.SRCALPHA)
            pygame.draw.line(aig, ROUGE, (5, 40), (5, 0), 3)
            aig = pygame.transform.rotate(aig, -obj.deg)
        virtual_screen.blit(aig, aig.get_rect(center=(obj.x + obj.L//2, obj.y + obj.l - 10)))
    else:
        t = font.render(str(obj.valeur), True, NOIR)
        virtual_screen.blit(t, t.get_rect(center=bx.center))


# ── Timers ─────────────────────────────────────────────────────────────────────

PHYSICS_REFRESH = pygame.USEREVENT + 1
FAST_REFRESH    = pygame.USEREVENT + 2
pygame.time.set_timer(PHYSICS_REFRESH, 1000)
pygame.time.set_timer(FAST_REFRESH,     500)

# ── Boucle ─────────────────────────────────────────────────────────────────────

running = True
while running:
    virtual_screen.fill(BLANC)
    try:
        bi = pygame.image.load("img/fond.png")
        virtual_screen.blit(pygame.transform.scale(bi, (VIRTUAL_W, VIRTUAL_H)), (0, 0))
    except Exception:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave()

        if event.type == PHYSICS_REFRESH:
            unit.refresh()
            if bg == 0:
                plan["power"].change_valeur(f"Power: {round(unit.thermal_power(), 2)}%")
                plan["period"].change_valeur(f"Period: {round(unit.period(), 1)}s")
                plan["temp"].change_valeur(f"Temp: {round(unit.reactor.temperature(), 1)}C")
                plan["pressure"].change_valeur(f"Press: {round(unit.reactor.pressure)}")
                plan["level"].change_valeur(f"Level: {round(unit.reactor.water_level(), 1)}")
                #plan["jauge_power"].change_valeur(min(100, unit.thermal_power()))
            update_turbine_screen()
            pygame.time.set_timer(PHYSICS_REFRESH, 1000)

        if event.type == FAST_REFRESH:
            if bg == 0:
                if rods_state == 1:
                    unit.raise_rods(rodsLists)
                elif rods_state == -1:
                    unit.lower_rods(rodsLists)
                change_rod_value()
            process_hold_buttons()
            unit.fast_refresh()
            pygame.time.set_timer(FAST_REFRESH, 500)

    for obj in plan.values():
        bx = pygame.Rect(obj.x, obj.y, obj.L, obj.l)
        if isinstance(obj, HoldButton):
            bouton_hold(obj, bx)
        elif isinstance(obj, Impulsion):
            bouton_impulsion(obj, bx)
        elif isinstance(obj, (Poussoir, Levier)):
            if not pygame.mouse.get_pressed()[0]:
                obj.clicked = True
            if bouton(obj, bx):
                if not obj.on:
                    obj.func(obj.arg)
                else:
                    obj.func2(obj.arg2)
                obj.clicked = False
                obj.on = not obj.on
        elif isinstance(obj, Afficheur):
            panneau(obj, bx)

    scaled = pygame.transform.smoothscale(
        virtual_screen, (int(VIRTUAL_W * scale), int(VIRTUAL_H * scale))
    )
    ecran.fill((0, 0, 0))
    ecran.blit(scaled, (0, 0))
    pygame.display.update()
    clock.tick(60)