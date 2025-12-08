
def objects(Poussoir, Afficheur, Levier, Jauge, antoine, unit, rodsLists, nothing, leave, barres):
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
        
        Afficheur(200,200,valeur="",nom="incr"),
        Afficheur(300,200,valeur="30°C", nom="temp"),
        Levier(400,200),
        Levier(500,200,func=unit.raise_rods,arg=rodsLists),

        Poussoir(700,550,nom="lever bars",func=barres,arg=1,verr=True,liens=["baisser bars","stopper bars"]),
        Poussoir(700,650,nom="stopper bars",func=barres,arg=0,on=True,verr=True,liens=["lever bars","baisser bars"]),
        Poussoir(700,750,nom="baisser bars",func=barres,arg=-1,verr=True,liens=["lever bars","stopper bars"]),

        Jauge(800,650,nom="jauge",MAX=10),
        Jauge(900,650,nom="voila",MAX=1)
    ]
    return objs