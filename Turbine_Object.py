# URSS's Grid Frequency = 50Hz
# Turbine rpm goal for 50Hz = 1500 rpm

class Turbine:
    """
    Turbine à vapeur avec physique réaliste.

    Modes :
      - mode=False : rotation libre — la vapeur accélère/décélère la turbine via l'inertie
      - mode=True  : rotation synchronisée — couplée au réseau, RPM forcé vers 1500 rpm

    Physique :
      - Modèle couple/inertie : τ_net = τ_vapeur - τ_frottement
      - dω/dt = τ_net / I  (I = moment d'inertie)
      - RPM → ω en rad/s, puis retour RPM
      - Puissance électrique = couple × ω × rendement (mode synchronisé seulement)
    """

    # ── Constantes physiques ──────────────────────────────────────────────────
    RPM_CIBLE       = 1500          # rpm réseau 50 Hz
    INERTIE         = 5000.0        # kg·m² — moment d'inertie de la turbine (lourd !)
    RENDEMENT       = 0.92          # rendement mécano-électrique
    FROTTEMENT_BASE = 0.08          # coefficient de frottement (N·m·s/rad)
    VAPEUR_COEFF    = 0.55          # conversion pression×ouverture → couple (N·m / unité)
    BYPASS_COEFF    = 0.10          # idem pour le bypass (moins efficace)
    SYNC_RIGIDITE   = 800.0         # N·m par rad/s d'écart en mode synchronisé
    DT              = 1.0           # pas de temps (1 s, cohérent avec reactor.refresh)

    def __init__(self):
        self.rpm   = 0.0            # tours par minute courants
        self._omega = 0.0           # rad/s interne (plus précis)

        # Mode : False = libre, True = synchronisé au réseau
        self.mode  = False

        # Valve principale
        self.valve_on = False
        self.valve    = 0.0         # position 0–100 %

        # Valve de contournement (bypass)
        self.bypass_on = False
        self.bypass    = 0.0        # position 0–100 %

        # Soupape de sûreté
        self.relief       = False
        self.relief_coeff = 2.0

        # Sorties calculées
        self.electrical_power = 0.0   # MW (valeur normalisée pour la démo)
        self.steam_consumed   = 0

    # ── Physique principale ───────────────────────────────────────────────────

    def refresh(self, pressure):
        """
        Appeler toutes les secondes avec la pression courante (en unités sim).
        Retourne la quantité de vapeur consommée (entier).
        """
        import math

        valve_frac  = self.valve  / 100.0
        bypass_frac = self.bypass / 100.0

        # Vapeur consommée par chaque chemin
        turbine_steam = valve_frac  * self.VAPEUR_COEFF  * pressure
        bypass_steam  = bypass_frac * self.BYPASS_COEFF  * pressure

        # ── Couple généré par la vapeur sur l'axe de la turbine ──
        # Le bypass ne fait pas tourner la turbine (il contourne)
        couple_vapeur = turbine_steam * pressure * 0.0005   # calibré pour monter en ~3–5 min

        # ── Couple de frottement (proportionnel à la vitesse) ──
        couple_frottement = self.FROTTEMENT_BASE * self._omega

        # ── Mode synchronisé : couple de rappel vers 1500 rpm ──
        omega_cible = self.RPM_CIBLE * 2 * math.pi / 60.0
        if self.mode:
            ecart = omega_cible - self._omega
            couple_sync = self.SYNC_RIGIDITE * ecart
        else:
            couple_sync = 0.0

        # ── Équation du mouvement : dω/dt = ΣF / I ──
        couple_net = couple_vapeur - couple_frottement + couple_sync
        domega = couple_net / self.INERTIE * self.DT

        self._omega = max(0.0, self._omega + domega)
        self.rpm    = self._omega * 60.0 / (2 * math.pi)

        # ── Puissance électrique (seulement si synchronisée) ──
        if self.mode:
            # P = τ_vapeur × ω × η  (normalisé en "%" pour la démo)
            P_meca = couple_vapeur * self._omega
            self.electrical_power = round(P_meca * self.RENDEMENT / 1e4, 2)  # unité arbitraire
        else:
            self.electrical_power = 0.0

        # ── Vapeur totale retirée du réacteur ──
        total_steam = int(turbine_steam + bypass_steam)
        self.steam_consumed = total_steam

        return total_steam

    # ── Valve principale ─────────────────────────────────────────────────────

    def valve_close(self):
        self.valve_on = False
        self.valve    = 0.0

    def valve_open(self, pressure):
        """N'ouvre que si la pression est suffisante."""
        if pressure < 4000:
            return
        self.valve_on = True

    def valve_setpoint(self, value):
        if self.valve_on:
            self.valve = max(0.0, min(100.0, float(value)))

    # ── Valve de contournement ────────────────────────────────────────────────

    def bypass_close(self):
        self.bypass_on = False
        self.bypass    = 0.0

    def bypass_open(self):
        self.bypass_on = True

    def bypass_setpoint(self, value):
        if self.bypass_on:
            self.bypass = max(0.0, min(100.0, float(value)))

    # ── Disjoncteur / synchronisation réseau ─────────────────────────────────

    def breaker(self):
        """
        Bascule le mode libre ↔ synchronisé.
        En mode réel, on ne connecte que si RPM ≈ 1500 ± 30 rpm.
        """
        if not self.mode:
            if self.check_condition():
                self.mode = True
        else:
            self.mode = False

    def check_condition(self):
        """Vérifie que la turbine est assez proche de 1500 rpm pour se coupler."""
        return abs(self.rpm - self.RPM_CIBLE) < 50   # tolérance ± 50 rpm

    # ── Accesseurs ───────────────────────────────────────────────────────────

    def get_rpm(self):
        return round(self.rpm, 1)

    def get_power(self):
        return self.electrical_power

    def is_sync(self):
        return self.mode