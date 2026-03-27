def objects(Poussoir, Afficheur, Levier, Jauge, Impulsion, HoldButton,
            antoine, unit, rodsLists, nothing, leave, barres, changeBg, bg):

    # ════════════════════════════════════════════════════════════════════
    #  BG = 0  — Écran réacteur
    #
    #  Layout 1920×1080 :
    #
    #  Gauche  (x=80–300)   : instruments — période, puissance, température
    #  Centre  (x=660–1260) : grille barres (boutons + afficheurs)
    #  Droite  (x=1550–1800): commandes barres (monter/stop/descendre)
    #  Bas centre           : navigation
    #
    #  Grille du cœur (hexagonale 6×6 avec masque) :
    #  Chaque cellule = 100px. Centre x=960, centre y=540.
    #  Disposition identique au masque dans Reactor_Object :
    #    rang0 (y=240): col2,col3          → 2 assemblages
    #    rang1 (y=340): col1,col2,col3,col4 → 4
    #    rang2 (y=440): col0..col5          → 6
    #    rang3 (y=540): col0..col5          → 6
    #    rang4 (y=640): col1..col4          → 4
    #    rang5 (y=740): col2,col3           → 2
    #
    #  Les boutons (sélection) sont en bas (y+BTN_OFFSET) des afficheurs.
    #  Numérotation : rod1..rod24 / B1..B24 dans le même ordre
    #  que change_rod_value() : c=24 décroissant, assemblage (0,2)..(5,3)
    #
    #  CORRECTION : les boutons sont inversés horizontalement ET verticalement
    #  par rapport aux afficheurs. On garde la même disposition pixel pour
    #  les afficheurs, mais on mappe les boutons en miroir (rang et col inversés).
    # ════════════════════════════════════════════════════════════════════

    # Coordonnées de la grille (centre de chaque cellule, ordre masque)
    CELL = 75          # pas entre cellules
    CX   = 910         # centre horizontal de la grille
    CY   = 50          # centre vertical de la grille (afficheurs)
    BTN_OFFSET = 500   # décalage vertical boutons sous les afficheurs

    # Masque du cœur — (rang, col) pour chaque assemblage dans l'ordre
    # de parcours de Reactor_Object (x=rang, y=col), soit rod24→rod1
    core_positions = [
        (0,2),(0,3),
        (1,1),(1,2),(1,3),(1,4),
        (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),
        (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),
        (4,1),(4,2),(4,3),(4,4),
        (5,2),(5,3),
    ]
    # rod24 = assemblage[0][2], rod23 = [0][3], ..., rod1 = [5][3]
    # change_rod_value() parcourt c=24→1, donc index 0 = rod24

    # Pour l'inversion des boutons : miroir horizontal (col → 5-col)
    # et vertical (rang → 5-rang)
    MAX_R = 5
    MAX_C = 5

    afficheurs_barres = []
    boutons_barres    = []
    for idx, (r, c) in enumerate(core_positions):
        rod_num = 24 - idx          # rod24 → rod1

        # Position pixel de l'afficheur (inchangée)
        px = CX + (c - 2.5) * CELL
        py = CY + r * CELL

        # Position pixel du bouton : rang et col inversés (miroir H+V)
        r_inv = MAX_R - r
        c_inv = MAX_C - c
        bx = CX + (c_inv - 2.5) * CELL
        by = CY + r_inv * CELL + BTN_OFFSET

        afficheurs_barres.append(
            Afficheur(int(px), int(py), L=70, l=44, nom=f"rod{rod_num}", valeur="0")
        )
        boutons_barres.append(
            Poussoir(int(bx), int(by), L=70, l=50,
                     func=antoine, arg=rod_num,
                     func2=antoine, arg2=rod_num,
                     label=f"B{rod_num}")
        )

    objs = [
        *afficheurs_barres,
        *boutons_barres,

        # ── Instruments gauche ────────────────────────────────────────
        # Période
        Afficheur( 80, 200, L=180, l=44, nom="period",  valeur="Period: --"),
        # Puissance thermique
        Afficheur( 80, 280, L=180, l=44, nom="power",   valeur="Power: 0%"),
        # Température eau
        Afficheur( 80, 360, L=180, l=44, nom="temp",    valeur="Temp: 30C"),
        # Pression
        Afficheur( 80, 440, L=180, l=44, nom="pressure",valeur="Press: 0"),
        # Niveau eau
        Afficheur( 80, 520, L=180, l=44, nom="level",   valeur="Level: --"),

        # ── Commandes barres — droite ─────────────────────────────────
        Poussoir(1650, 350, L=120, l=60, nom="lever bars",
                 func=barres, arg=1,  verr=True,
                 liens=["baisser bars", "stopper bars"],
                 label="Rod Up"),
        Poussoir(1650, 450, L=120, l=60, nom="stopper bars",
                 func=barres, arg=0,  on=True, verr=True,
                 liens=["lever bars", "baisser bars"],
                 label="Rod Stop"),
        Poussoir(1650, 550, L=120, l=60, nom="baisser bars",
                 func=barres, arg=-1, verr=True,
                 liens=["lever bars", "stopper bars"],
                 label="Rod Down"),

        # ── Jauges droite ─────────────────────────────────────────────
        Jauge(1650, 650, L=120, l=80, nom="jauge_power", MAX=100, valeur=0),
        Afficheur(1650, 750, L=120, l=44, nom="jauge_power_lbl", valeur="Power"),

        # ── Navigation ────────────────────────────────────────────────
        Impulsion(80, 980, L=160, l=50, nom="next",
                  func=changeBg, arg=bg+1, label="Turbine >>"),
        
        Impulsion(200, 980, L=160, l=50, nom="Quit",
                  func=leave, label="Quit"),
    ]

    # ════════════════════════════════════════════════════════════════════
    #  BG = 1  — Écran turbine
    #
    #  Layout 1920×1080 :
    #
    #  Colonne gauche  (x≈80)  : jauges RPM + puissance
    #  Colonne centre  (x≈700) : afficheurs état
    #  Colonne droite  (x≈1100): commandes vannes + disjoncteur
    #  Bas             (y≈950) : navigation
    #
    #  Vannes :
    #    - 1 Poussoir verrouillé "Open" / "Closed" (closed par défaut)
    #    - 4 HoldButtons réglage (lent/rapide ouv/ferm)
    #      → action répétée à chaque FAST_REFRESH (500ms) tant que maintenu
    #
    #  Disjoncteur : Poussoir toggle simple
    # ════════════════════════════════════════════════════════════════════

    def _valve_open(a=None):
        unit.turbine.valve_open(unit.reactor.pressure)

    def _valve_close(a=None):
        unit.turbine.valve_close()

    def _bypass_open(a=None):
        unit.turbine.bypass_open()

    def _bypass_close(a=None):
        unit.turbine.bypass_close()

    def _breaker(a=None):
        unit.turbine.breaker()

    # HoldButton — appelé à chaque FAST_REFRESH (500ms) tant que maintenu
    # ++ / -- : 1.0 % par tick   |   + / - : 0.5 % par tick
    def _v_fast_open(a=None):
        unit.turbine.valve_setpoint(unit.turbine.valve + 1.0)

    def _v_slow_open(a=None):
        unit.turbine.valve_setpoint(unit.turbine.valve + 0.5)

    def _v_slow_close(a=None):
        unit.turbine.valve_setpoint(unit.turbine.valve - 0.5)

    def _v_fast_close(a=None):
        unit.turbine.valve_setpoint(unit.turbine.valve - 1.0)

    def _b_fast_open(a=None):
        unit.turbine.bypass_setpoint(unit.turbine.bypass + 1.0)

    def _b_slow_open(a=None):
        unit.turbine.bypass_setpoint(unit.turbine.bypass + 0.5)

    def _b_slow_close(a=None):
        unit.turbine.bypass_setpoint(unit.turbine.bypass - 0.5)

    def _b_fast_close(a=None):
        unit.turbine.bypass_setpoint(unit.turbine.bypass - 1.0)

    # Largeur bouton vanne
    BW = 90   # largeur
    BH = 60   # hauteur

    # ── Positions colonne commandes vannes ────────────────────────────
    VX  = 1100  # x colonne commandes
    VY1 = 160   # y bloc valve
    VY2 = 460   # y bloc bypass
    VY3 = 760   # y disjoncteur

    # Boutons open/close : côte à côte
    # 4 hold : côte à côte en dessous
    BX_OPENCLOSE = [VX, VX + BW + 10]
    BX_HOLD      = [VX + i*(BW+8) for i in range(4)]

    objs2 = [
        # ── Jauges analogiques ────────────────────────────────────────
        Jauge(80, 150, L=120, l=80, nom="turb_rpm",   MAX=1500, valeur=0),
        Afficheur(80, 250, L=120, l=44, nom="turb_rpm_num", valeur="0 rpm"),
        Afficheur(80, 310, L=120, l=30, nom="turb_rpm_lbl", valeur="RPM"),

        Jauge(80, 400, L=120, l=80, nom="turb_power", MAX=100, valeur=0),
        Afficheur(80, 500, L=120, l=44, nom="turb_power_num", valeur="0 MW"),
        Afficheur(80, 550, L=120, l=30, nom="turb_power_lbl", valeur="Power"),

        # ── Afficheurs état (centre) ──────────────────────────────────
        Afficheur(600, 160, L=250, l=50, nom="turb_valve_num",    valeur="Valve: 0.0%"),
        Afficheur(600, 230, L=250, l=50, nom="turb_bypass_num",   valeur="Bypass: 0.0%"),
        Afficheur(600, 300, L=250, l=50, nom="turb_pressure_num", valeur="Press: 0"),
        Afficheur(600, 370, L=250, l=50, nom="turb_sync",         valeur="FREE"),
        Afficheur(600, 440, L=250, l=50, nom="turb_breaker_state",valeur="OFF GRID"),

        # ══════════════════════════════════════════════════════════════
        #  VALVE PRINCIPALE
        # ══════════════════════════════════════════════════════════════

        Afficheur(VX, VY1 - 50, L=200, l=40, nom="valve_title", valeur="Main Valve"),

        # Open / Closed — Poussoir verrouillé, Closed ON par défaut
        Poussoir(BX_OPENCLOSE[0], VY1, L=BW, l=BH,
                 nom="valve_open",
                 func=_valve_open, arg=None,
                 func2=nothing,    arg2=None,
                 on=False, verr=True,
                 liens=["valve_close"],
                 label="Open"),
        Poussoir(BX_OPENCLOSE[1], VY1, L=BW, l=BH,
                 nom="valve_close",
                 func=_valve_close, arg=None,
                 func2=nothing,     arg2=None,
                 on=True, verr=True,
                 liens=["valve_open"],
                 label="Closed"),

        # 4 HoldButtons réglage — action répétée au FAST_REFRESH tant que maintenu
        HoldButton(BX_HOLD[0], VY1 + BH + 20, L=BW, l=BH,
                   nom="v_fast_open",  func=_v_fast_open,  label="++ Open"),
        HoldButton(BX_HOLD[1], VY1 + BH + 20, L=BW, l=BH,
                   nom="v_slow_open",  func=_v_slow_open,  label="+ Open"),
        HoldButton(BX_HOLD[2], VY1 + BH + 20, L=BW, l=BH,
                   nom="v_slow_close", func=_v_slow_close, label="- Close"),
        HoldButton(BX_HOLD[3], VY1 + BH + 20, L=BW, l=BH,
                   nom="v_fast_close", func=_v_fast_close, label="-- Close"),

        # ══════════════════════════════════════════════════════════════
        #  BYPASS
        # ══════════════════════════════════════════════════════════════

        Afficheur(VX, VY2 - 50, L=200, l=40, nom="bypass_title", valeur="Bypass"),

        Poussoir(BX_OPENCLOSE[0], VY2, L=BW, l=BH,
                 nom="bypass_open",
                 func=_bypass_open, arg=None,
                 func2=nothing,     arg2=None,
                 on=False, verr=True,
                 liens=["bypass_close"],
                 label="Open"),
        Poussoir(BX_OPENCLOSE[1], VY2, L=BW, l=BH,
                 nom="bypass_close",
                 func=_bypass_close, arg=None,
                 func2=nothing,      arg2=None,
                 on=True, verr=True,
                 liens=["bypass_open"],
                 label="Closed"),

        HoldButton(BX_HOLD[0], VY2 + BH + 20, L=BW, l=BH,
                   nom="b_fast_open",  func=_b_fast_open,  label="++ Open"),
        HoldButton(BX_HOLD[1], VY2 + BH + 20, L=BW, l=BH,
                   nom="b_slow_open",  func=_b_slow_open,  label="+ Open"),
        HoldButton(BX_HOLD[2], VY2 + BH + 20, L=BW, l=BH,
                   nom="b_slow_close", func=_b_slow_close, label="- Close"),
        HoldButton(BX_HOLD[3], VY2 + BH + 20, L=BW, l=BH,
                   nom="b_fast_close", func=_b_fast_close, label="-- Close"),

        # ══════════════════════════════════════════════════════════════
        #  DISJONCTEUR RÉSEAU — Poussoir toggle simple
        # ══════════════════════════════════════════════════════════════

        Afficheur(VX, VY3 - 50, L=200, l=40, nom="breaker_title", valeur="Grid"),

        Poussoir(VX, VY3, L=BW*2+10, l=BH,
                 nom="breaker",
                 func=_breaker, arg=None,
                 func2=_breaker, arg2=None,
                 on=False, verr=False, liens=[],
                 label="Breaker"),

        # ── Navigation ────────────────────────────────────────────────
        Impulsion(80, 980, L=160, l=50, nom="back",
                  func=changeBg, arg=bg-1, label="<< Reactor"),
    ]

    o = objs if bg == 0 else objs2 if bg == 1 else []

    plan = {}
    for i, obj in enumerate(o):
        nom = obj.nom if obj.nom != "bo" else str(i)
        plan[nom] = obj
    return plan