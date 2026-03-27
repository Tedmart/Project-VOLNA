# URSS's Grid Frequency = 50Hz
# Turbine rpm goal for 50Hz = 1500 rpm

class Turbine:
    """
    Turbine à vapeur avec physique réaliste.

    ── GUIDE DE RÉGLAGE ──────────────────────────────────────────────────────

    Accélération (valve ouverte) :
      → COUPLE_COEFF ↑  : accélère plus vite (levier principal)
      → INERTIE ↓       : monte plus vite
      Tableau COUPLE_COEFF (INERTIE=2000) :
        0.001 → ~5 min | 0.003 → ~2 min | 0.008 → ~45 s | 0.02 → ~20 s
      Valeur actuelle : 0.005 → ~1 min 30 s à pression nominale

    Décélération (valve fermée) :
      → FROTTEMENT_BASE ↑ : freine plus fort (levier principal)
      → FROTTEMENT_VISCO ↑: frein quadratique (plus fort à haute vitesse)
      Tableau FROTTEMENT_BASE (INERTIE=2000) :
        0.5  → freine en ~5 min | 2.0 → ~1 min | 5.0 → ~30 s
      Valeur actuelle : 3.0 → ~45 s

    Pression minimale d'ouverture valve : 4000 hPa
    ──────────────────────────────────────────────────────────────────────────
    """

    RPM_CIBLE        = 1500
    INERTIE          = 2000.0   # kg·m²   ↓ = monte/descend plus vite
    RENDEMENT        = 0.92
    FROTTEMENT_BASE  = 3.0      # N·m·s/rad  — freine en ~45 s (était 2.0 → ~1 min)
    FROTTEMENT_VISCO = 0.002    # N·m·s²/rad² — frein quadratique renforcé (était 0.001)
    VAPEUR_COEFF     = 0.55
    BYPASS_COEFF     = 0.10
    COUPLE_COEFF     = 0.005    # accélère en ~1 min 30 s (était 0.003 → ~2 min)
    SYNC_RIGIDITE    = 800.0
    DT               = 1.0

    def __init__(self):
        self.rpm    = 0.0
        self._omega = 0.0

        self.mode   = False

        self.valve_on = False
        self.valve    = 0.0

        self.bypass_on = False
        self.bypass    = 0.0

        self.relief       = False
        self.relief_coeff = 2.0

        self.electrical_power = 0.0
        self.steam_consumed   = 0

    def refresh(self, pressure):
        import math

        valve_frac  = self.valve  / 100.0
        bypass_frac = self.bypass / 100.0

        turbine_steam = valve_frac  * self.VAPEUR_COEFF  * pressure
        bypass_steam  = bypass_frac * self.BYPASS_COEFF  * pressure

        couple_vapeur = turbine_steam * pressure * self.COUPLE_COEFF

        # Frottement combiné : linéaire + quadratique
        couple_frottement = (
            self.FROTTEMENT_BASE * self._omega
            + self.FROTTEMENT_VISCO * self._omega ** 2
        )

        omega_cible = self.RPM_CIBLE * 2 * math.pi / 60.0
        couple_sync = self.SYNC_RIGIDITE * (omega_cible - self._omega) if self.mode else 0.0

        couple_net  = couple_vapeur - couple_frottement + couple_sync
        self._omega = max(0.0, self._omega + couple_net / self.INERTIE * self.DT)
        self.rpm    = self._omega * 60.0 / (2 * math.pi)

        if self.mode:
            self.electrical_power = round(
                couple_vapeur * self._omega * self.RENDEMENT / 1e4, 2
            )
        else:
            self.electrical_power = 0.0

        total_steam = int(turbine_steam + bypass_steam)
        self.steam_consumed = total_steam
        return total_steam

    # ── Valve principale ──────────────────────────────────────────────────────

    def valve_close(self):
        self.valve_on = False
        self.valve    = 0.0

    def valve_open(self, pressure):
        if pressure < 4000:
            return False
        self.valve_on = True
        return True

    def valve_setpoint(self, value):
        if self.valve_on:
            self.valve = max(0.0, min(100.0, float(value)))

    # ── Bypass ────────────────────────────────────────────────────────────────

    def bypass_close(self):
        self.bypass_on = False
        self.bypass    = 0.0

    def bypass_open(self):
        self.bypass_on = True

    def bypass_setpoint(self, value):
        if self.bypass_on:
            self.bypass = max(0.0, min(100.0, float(value)))

    # ── Disjoncteur ───────────────────────────────────────────────────────────

    def breaker(self):
        if not self.mode:
            if self.check_condition():
                self.mode = True
        else:
            self.mode = False

    def check_condition(self):
        return abs(self.rpm - self.RPM_CIBLE) < 50

    # ── Accesseurs ────────────────────────────────────────────────────────────

    def get_rpm(self):
        return round(self.rpm, 1)

    def get_power(self):
        return self.electrical_power

    def is_sync(self):
        return self.mode