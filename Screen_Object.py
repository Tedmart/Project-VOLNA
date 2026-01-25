
def objects(Poussoir, Afficheur, Levier, Jauge, antoine, unit, rodsLists, nothing, leave, barres, changeBg, bg):
    objs = [
        
        Poussoir(200,710,func=antoine,arg=1,func2=antoine,arg2=1),
        Poussoir(300,710,func=antoine,arg=2,func2=antoine,arg2=2),

        Poussoir(100,770,func=antoine,arg=3,func2=antoine,arg2=3),
        Poussoir(200,770,func=antoine,arg=4,func2=antoine,arg2=4),
        Poussoir(300,770,func=antoine,arg=5,func2=antoine,arg2=5),
        Poussoir(400,770,func=antoine,arg=6,func2=antoine,arg2=6),

        Poussoir(0,830,func=antoine,arg=7,func2=antoine,arg2=7),
        Poussoir(100,830,func=antoine,arg=8,func2=antoine,arg2=8),
        Poussoir(200,830,func=antoine,arg=9,func2=antoine,arg2=9),
        Poussoir(300,830,func=antoine,arg=10,func2=antoine,arg2=10),
        Poussoir(400,830,func=antoine,arg=11,func2=antoine,arg2=11),
        Poussoir(500,830,func=antoine,arg=12,func2=antoine,arg2=12),

        Poussoir(0,890,func=antoine,arg=13,func2=antoine,arg2=13),
        Poussoir(100,890,func=antoine,arg=14,func2=antoine,arg2=14),
        Poussoir(200,890,func=antoine,arg=15,func2=antoine,arg2=15),
        Poussoir(300,890,func=antoine,arg=16,func2=antoine,arg2=16),
        Poussoir(400,890,func=antoine,arg=17,func2=antoine,arg2=17),
        Poussoir(500,890,func=antoine,arg=18,func2=antoine,arg2=18),

        Poussoir(100,950,func=antoine,arg=19,func2=antoine,arg2=19),
        Poussoir(200,950,func=antoine,arg=20,func2=antoine,arg2=20),
        Poussoir(300,950,func=antoine,arg=21,func2=antoine,arg2=21),
        Poussoir(400,950,func=antoine,arg=22,func2=antoine,arg2=22),
        
        Poussoir(200,1010,func=antoine,arg=23,func2=antoine,arg2=23),
        Poussoir(300,1010,func=antoine,arg=24,func2=antoine,arg2=24),


        Afficheur(200, 550, valeur="0", nom="rod1"),
        Afficheur(300, 550, valeur="0", nom="rod2"),

        Afficheur(100, 500, valeur="0", nom="rod3"),
        Afficheur(200, 500, valeur="0", nom="rod4"),
        Afficheur(300, 500, valeur="0", nom="rod5"),
        Afficheur(400, 500, valeur="0", nom="rod6"),

        Afficheur(00, 450, valeur="0", nom="rod7"),
        Afficheur(100, 450, valeur="0", nom="rod8"),
        Afficheur(200, 450, valeur="0", nom="rod9"),
        Afficheur(300, 450, valeur="0", nom="rod10"),
        Afficheur(400, 450, valeur="0", nom="rod11"),
        Afficheur(500, 450, valeur="0", nom="rod12"),

        Afficheur(00, 400, valeur="0", nom="rod13"),
        Afficheur(100, 400, valeur="0", nom="rod14"),
        Afficheur(200, 400, valeur="0", nom="rod15"),
        Afficheur(300, 400, valeur="0", nom="rod16"),
        Afficheur(400, 400, valeur="0", nom="rod17"),
        Afficheur(500, 400, valeur="0", nom="rod18"),
        
        Afficheur(100, 350, valeur="0", nom="rod19"),
        Afficheur(200, 350, valeur="0", nom="rod20"),
        Afficheur(300, 350, valeur="0", nom="rod21"),
        Afficheur(400, 350, valeur="0", nom="rod22"),

        Afficheur(200, 300, valeur="0", nom="rod23"),
        Afficheur(300, 300, valeur="0", nom="rod24"),


        
        Afficheur(200,200,valeur="",nom="period"),
        Afficheur(300,200,valeur="30°C", nom="power"),
        Levier(400,200),
        Levier(500,200,func=unit.raise_rods,arg=rodsLists),

        Poussoir(700,550,nom="lever bars",func=barres,arg=1,verr=True,liens=["baisser bars","stopper bars"]),
        Poussoir(700,650,nom="stopper bars",func=barres,arg=0,on=True,verr=True,liens=["lever bars","baisser bars"]),
        Poussoir(700,750,nom="baisser bars",func=barres,arg=-1,verr=True,liens=["lever bars","stopper bars"]),

        Jauge(800,650,nom="jauge",MAX=10),
        Jauge(900,650,nom="voila",MAX=1),

        Poussoir(1000,600,nom="next",func=changeBg,arg=bg+1)
    ]

    objs2 = [
        Jauge(1200,150,nom="jauge",MAX=10),

        Poussoir(1000,600,nom="back",func=changeBg,arg=bg-1),
    ]

    o = []
    plan = {}

    if bg == 0:
        o = objs
    elif bg == 1:
        o = objs2

    
    for i, obj in enumerate(o):
        nom = obj.nom if obj.nom != "bo" else str(i)
        plan[nom]=obj

    return plan

