import pygame
import sys
import Unit_Object


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
def leave(a=None):
    running = False
    pygame.quit()
    sys.exit()

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
    def __init__(self,x,y,L=50,l=50,type="img/poussoir.png",typeBis="img/poussoir_.png",nom="bo",func=leave,arg="oui",func2=nothing,arg2=None):
        Sprite.__init__(self,x,y,L,l,type,nom)
        self.clicked=False
        self.on=False
        self.typeBis=typeBis
        self.func=func
        self.arg=arg
        self.func2=func2
        self.arg2=arg2

    def __repr__(self):
        return f"Poussoir({self.x},{self.y},{self.type},{self.nom},{self.func})"

class Levier(Sprite):
    def __init__(self,x,y,L=20,l=37,type="img/levier.png",typeBis="img/levier_.png",nom="bo",func=leave,arg="non",func2=nothing,arg2=None):
        Sprite.__init__(self,x,y,L,l,type,nom)
        self.clicked=False
        self.on=False
        self.typeBis=typeBis
        self.func=func
        self.arg=arg
        self.func2=func2
        self.arg2=arg2

    def __repr__(self):
        return f"Levier({self.x},{self.y},{self.type},{self.nom},{self.func})"

class Afficheur(Sprite):
    def __init__(self,x,y,L=56,l=44,type="img/num.png",nom="bo",valeur=0):
        Sprite.__init__(self,x,y,L,l,type,nom)
        self.valeur=valeur

    def change_valeur(self,valeur):
        self.valeur = valeur

    def __repr__(self):
        return f"Afficheur({self.x},{self.y},{self.type},{self.valeur},{self.nom})"
        

# --- Initialisation ---
pygame.init()
running = True

# --- Paramètres de la fenêtre ---
LARGEUR=1920
HAUTEUR=1080
ecran = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Projet : VOLNA")
# --- Police ---
font = pygame.font.SysFont(None, 36)
# --- Sprites ---

objs = [
    Poussoir(200,400,func=antoine,arg=1,func2=antoine,arg2=1),
    Poussoir(300,400,func=antoine,arg=2,func2=antoine,arg2=2),

    Poussoir(100,500,func=antoine,arg=3,func2=antoine,arg2=3),
    Poussoir(200,500,func=antoine,arg=4,func2=antoine,arg2=4),
    Poussoir(300,500,func=antoine,arg=5,func2=antoine,arg2=5),
    Poussoir(400,500,func=antoine,arg=6,func2=antoine,arg2=6),

    Poussoir(0,600,func=antoine,arg=7,func2=antoine,arg2=7),
    Poussoir(100,600,func=antoine,arg=8,func2=antoine,arg2=8),
    Poussoir(200,600,func=antoine,arg=9,func2=antoine,arg2=9),
    Poussoir(300,600,func=antoine,arg=10,func2=antoine,arg2=10),
    Poussoir(400,600,func=antoine,arg=11,func2=antoine,arg2=11),
    Poussoir(500,600,func=antoine,arg=12,func2=antoine,arg2=12),

    Poussoir(0,700,func=antoine,arg=13,func2=antoine,arg2=13),
    Poussoir(100,700,func=antoine,arg=14,func2=antoine,arg2=14),
    Poussoir(200,700,func=antoine,arg=15,func2=antoine,arg2=15),
    Poussoir(300,700,func=antoine,arg=16,func2=antoine,arg2=16),
    Poussoir(400,700,func=antoine,arg=17,func2=antoine,arg2=17),
    Poussoir(500,700,func=antoine,arg=18,func2=antoine,arg2=18),

    Poussoir(100,800,func=antoine,arg=19,func2=antoine,arg2=19),
    Poussoir(200,800,func=antoine,arg=20,func2=antoine,arg2=20),
    Poussoir(300,800,func=antoine,arg=21,func2=antoine,arg2=21),
    Poussoir(400,800,func=antoine,arg=22,func2=antoine,arg2=22),
    
    Poussoir(200,900,func=antoine,arg=23,func2=antoine,arg2=23),
    Poussoir(300,900,func=antoine,arg=24,func2=antoine,arg2=24),
    
    Afficheur(200,200,valeur=0,nom="incr"),
    Afficheur(300,200,valeur="59°C"),
    Levier(400,200),
    Levier(500,200,func=unit.raise_rods,arg=rodsLists)
]

# --- Plans ---
plan = {}
i=0
for obj in objs:
    i+=1
    nom = obj.nom if obj.nom != "bo" else str(i)
    plan[nom]=obj


clock = pygame.time.Clock()  # stabilise les FPS

def bouton(obj):
    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()[0]
    clicked = obj.clicked
    
    # Changement de sprite au survol
    #type = pygame.image.load(obj.typeBis) if box.collidepoint(souris) or obj.on else pygame.image.load(obj.type)
    # Changement de sprite si est activé
    type = pygame.image.load(obj.typeBis) if obj.on else pygame.image.load(obj.type)
    ecran.blit(type, box)
    
    return clic and box.collidepoint(souris) and clicked

def panneau(obj):
    type = pygame.image.load(obj.type)
    #pygame.draw.rect(ecran, couleur, box)
    ecran.blit(type, box)
    texte = font.render(str(obj.valeur), True, NOIR)
    texte_rect = texte.get_rect(center=box.center)
    ecran.blit(texte, texte_rect)

# --- Boucle principale ---
i=0
PHYSICS_REFRESH = pygame.USEREVENT + 1
FAST_REFRESH = pygame.USEREVENT + 2

pygame.time.set_timer(PHYSICS_REFRESH, 1000)
pygame.time.set_timer(FAST_REFRESH, 500)

while running:
    i+=1
    ecran.fill(BLANC)
    BG = pygame.image.load("img/myimage.jpg")
    BGrect = BG.get_rect()
    ecran.blit(BG, BGrect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT : leave()
        if event.type == PHYSICS_REFRESH:
            #ma_fonction()
            unit.refresh()
            pygame.time.set_timer(PHYSICS_REFRESH, 1000)

        if event.type == FAST_REFRESH:
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
                

    pygame.display.update()
    clock.tick(60)
