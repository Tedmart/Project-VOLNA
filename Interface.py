import pygame
import sys
import Unit_Object
from Screen_Object import objects


unit = Unit_Object.Unit()


"""
différent type de bouton, comme un switch par exemple
différent type d'affichage (aiguille)
"""
# --- Couleurs ---
BLANC = (255, 255, 255)
GRIS = (180, 180, 180)
GRIS_FONCE = (140, 140, 140)
NOIR = (0, 0, 0)
ROUGE = (255,0,0)
GOLD = (255,215,0)
BLEU = (0,0,255)

i=0
rodsLists = [False for i in range(24)]
rods_state = 0

def leave(a=None):
    running = False
    pygame.quit()
    sys.exit()

def barres(a):
    global rods_state
    rods_state = a

def incr(a):
    plan["incr"].change_valeur(a)

def nothing(a=None):
    pass

def antoine(a=None):
    rodsLists[a-1]= not rodsLists[a-1]

def afficherLst(a=None):
    print(rodsLists)

class Sprite:
    def __init__(self,x,y,L=40,l=20,type="img/type.png",nom="bo"):
        self.x=x
        self.y=y
        self.L=L
        self.l=l
        self.type=type
        self.nom=nom

    def __repr__(self):
        return f"Sprite({self.x},{self.y},{self.L},{self.l},{self.type},{self.nom})"

class Poussoir(Sprite):
    def __init__(self,x,y,L=50,l=50,type="img/poussoir.png",typeBis="img/poussoir_.png",nom="bo",func=leave,arg="oui",func2=nothing,arg2=None,on=False,verr=False,liens=[]):
        Sprite.__init__(self,x,y,L,l,type,nom)
        self.clicked=False
        self.on=on
        self.typeBis=typeBis
        self.func=func
        self.arg=arg
        self.func2=func2
        self.arg2=arg2
        self.liens=liens
        self.verr=verr

    def __repr__(self):
        return f"Poussoir({self.x},{self.y},{self.type},{self.nom},{self.func},{self.liens})"

    def switch(self):
        self.on = not self.on
        self.func2(self.arg2)

class Levier(Poussoir):
    def __init__(self,x,y,L=20,l=37,type="img/levier.png",typeBis="img/levier_.png",nom="bo",func=leave,arg="non",func2=nothing,arg2=None,on=False,verr=False,liens=[]):
        Poussoir.__init__(self,x,y,L,l,type,typeBis,nom,func,arg,func2,arg2,on,verr,liens)
        
    def __repr__(self):
        return f"Levier({self.x},{self.y},{self.type},{self.nom},{self.func},{self.liens})"

class Afficheur(Sprite):
    def __init__(self,x,y,L=56,l=44,type="img/num.png",nom="bo",valeur=0):
        Sprite.__init__(self,x,y,L,l,type,nom)
        self.valeur=valeur

    def change_valeur(self,valeur):
        self.valeur = valeur

    def __repr__(self):
        return f"Afficheur({self.x},{self.y},{self.type},{self.valeur},{self.nom})"

class Jauge(Afficheur):
    def __init__(self,x,y,L=70,l=49,type="img/cadrant.png",nom="bo",valeur=0,MAX=10):
        Afficheur.__init__(self,x,y,L,l,type,nom,valeur)
        self.MAX=MAX
        deg = 0
        self.deg=deg
    def change_valeur(self,valeur):
        self.valeur = valeur
        MAX = self.MAX
        valeur = valeur%MAX
        self.deg=int(round((valeur/MAX)*180,0))
        print(self.deg)
        
# --- Initialisation ---
pygame.init()
running = True

# --- Résolution virtuelle ---
VIRTUAL_W = 1920
VIRTUAL_H = 1080

# Résolution réelle de l'écran
real_w = pygame.display.Info().current_w
real_h = pygame.display.Info().current_h

# Facteur de scale
scale_x = real_w / VIRTUAL_W
scale_y = real_h / VIRTUAL_H
scale = min(scale_x, scale_y)

# Surface virtuelle (où tout est dessiné)
virtual_screen = pygame.Surface((VIRTUAL_W, VIRTUAL_H))

# Fenêtre réelle
ecran = pygame.display.set_mode((real_w, real_h))


pygame.display.set_caption("Projet : VOLNA")
# --- Police ---
font = pygame.font.SysFont(None, 36)
# --- Sprites ---

objs = objects(Poussoir, Afficheur, Levier, Jauge, antoine, unit, rodsLists, nothing, leave, barres)

# --- Plans ---
plan = {}
i=0 
for obj in objs:
    i+=1
    nom = obj.nom if obj.nom != "bo" else str(i)
    plan[nom]=obj


clock = pygame.time.Clock()  # stabilise les FPS

def bouton(obj):
    # Adapter la souris à la résolution virtuelle
    souris = (
        pygame.mouse.get_pos()[0] / scale,
        pygame.mouse.get_pos()[1] / scale
    )

    clic = pygame.mouse.get_pressed()[0]
    clicked = obj.clicked
    
    # Changement de sprite au survol
    #type = pygame.image.load(obj.typeBis) if box.collidepoint(souris) or obj.on else pygame.image.load(obj.type)
    # Changement de sprite si est activé
    type = pygame.image.load(obj.typeBis) if obj.on else pygame.image.load(obj.type)
    virtual_screen.blit(type, box)

    if clic and box.collidepoint(souris) and clicked:
        for lien in obj.liens:
            btn = plan[lien]
            if not obj.on and btn.on:
                btn.switch()
    if obj.on and obj.verr:
        return False
    return clic and box.collidepoint(souris) and clicked

def panneau(obj):
    type = pygame.image.load(obj.type)
    #pygame.draw.rect(ecran, couleur, box)
    virtual_screen.blit(type, box)
    if isinstance(obj,Jauge):
        img = "img/aiguille.png"
        l = 70
        L = 10
        aig = pygame.transform.rotate(pygame.image.load(img), -obj.deg)
        new_rect = aig.get_rect(center = aig.get_rect(center = (obj.x+(obj.L/2), obj.y+obj.l-L)).center)
        virtual_screen.blit(aig, new_rect)
    else:
        texte = font.render(str(obj.valeur), True, NOIR)
        texte_rect = texte.get_rect(center=box.center)
        virtual_screen.blit(texte, texte_rect)

# --- Boucle principale ---
i=0
PHYSICS_REFRESH = pygame.USEREVENT + 1
FAST_REFRESH = pygame.USEREVENT + 2

pygame.time.set_timer(PHYSICS_REFRESH, 1000)
pygame.time.set_timer(FAST_REFRESH, 500)

while running:
    plan["jauge"].change_valeur(i)
    plan["voila"].change_valeur(1)
    i+=1
    # On dessine dans la surface
    virtual_screen.fill(BLANC)

    BG = pygame.image.load("img/myimage.jpg")
    BG = pygame.transform.scale(BG, (VIRTUAL_W, VIRTUAL_H))
    virtual_screen.blit(BG, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT : leave()
        if event.type == PHYSICS_REFRESH:
            #ma_fonction()
            unit.refresh()
            plan["temp"].change_valeur(f"{round(unit.temperature(), 0)}°C")
            pygame.time.set_timer(PHYSICS_REFRESH, 1000)

        if event.type == FAST_REFRESH:
            if rods_state == 1:
                unit.raise_rods(rodsLists)
            elif rods_state == -1:
                unit.lower_rods(rodsLists)
            plan["incr"].change_valeur(f"{round(unit.reactor.assembly[0][0].rods_pulled, 3)}")
            unit.fast_refresh()
            pygame.time.set_timer(FAST_REFRESH, 500)
            
    for obj in plan.values():
        box=pygame.Rect(obj.x,obj.y,obj.L,obj.l)
        if isinstance(obj, Poussoir) or isinstance(obj, Levier):
            if not pygame.mouse.get_pressed()[0] : obj.clicked = True
            if bouton(obj):
                if not obj.on:
                    obj.func(obj.arg)  # <-- Execution de la fonction 1 du bouton
                else:
                    obj.func2(obj.arg2) # <-- Execution de la fonction 2 du bouton
                obj.clicked = False
                obj.on = not obj.on
        if isinstance(obj, Afficheur):
            panneau(obj)


    # ---- SCALE FINAL ----
    scaled_surface = pygame.transform.smoothscale(
        virtual_screen,
        (int(VIRTUAL_W * scale), int(VIRTUAL_H * scale))
    )

    # On efface la fenêtre réelle (pas necessaire à cause du fond d'écran mais on sait jamais)
    ecran.fill((0, 0, 0))

    # On dessine la surface virtuelle mise à l'échelle
    ecran.blit(scaled_surface, (0, 0))

                

    pygame.display.update()
    clock.tick(60)
