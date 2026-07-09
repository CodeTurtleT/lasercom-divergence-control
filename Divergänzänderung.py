# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:44:33 2026

@author: pboe
"""

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Gegebene Parameter
# -----------------------------
lam  = 1064e-9   # Wellenlänge [m]
M2   = 1.3       # Strahlqualitätsfaktor (1.0 = idealer Gaußstrahl)
MFD  = 5.4e-6    # Mode Field Diameter [m]
wf   = MFD / 2   # Waist-Radius am Faserende [m]
f    = 36.6e-3   # Brennweite [m]

# Effektive Wellenlänge für M²-Strahl
lam_eff = M2 * lam   # [m]  

# Rayleigh-Länge am Faserwaist (mit M²)
zR = np.pi * wf**2 / lam_eff   # [m]

# Delta-Bereich: +/- 1 mm
delta = np.linspace(-1e-3, 1e-3, 1001)
s = f + delta   # Abstand Faser -> Linse [m]

# -----------------------------
# Strahlradius an der Linse
# -----------------------------
w_lens = wf * np.sqrt(1 + (s / zR)**2)
d_lens = 2 * w_lens

# -----------------------------
# q-Parameter vor und nach der Linse
# (ABCD-Transformation unverändert)
# -----------------------------
q1 = s + 1j * zR
q2 = 1 / (1 / q1 - 1 / f)

z_waist = -np.real(q2)   # Neue Waist-Position [m]
zR_new  =  np.imag(q2)   # Neue Rayleigh-Länge  [m]

# Neuer Waist-Radius (mit M²)
w0_new = np.sqrt(lam_eff * zR_new / np.pi)   # 
d0_new = 2 * w0_new

# Divergenz (Halbwinkel, mit M²)
theta      = lam_eff / (np.pi * w0_new)   # [rad]  
theta_mrad = theta * 1e3                  # [mrad]

# -----------------------------
# Strahlgröße bei gegebenen Distanzen
# -----------------------------
z1 = 1e3      # 1 km  [m]
z2 = 500e3    # 500 km [m]

w_1km   = w0_new * np.sqrt(1 + ((z1 - z_waist) / zR_new)**2)
d_1km   = 2 * w_1km

w_500km = w0_new * np.sqrt(1 + ((z2 - z_waist) / zR_new)**2)
d_500km = 2 * w_500km

# -----------------------------
# Ausgabe bei Delta = 0
# -----------------------------
idx0 = np.argmin(np.abs(delta))

print("Parameter:")
print(f"  lambda      = {lam*1e9:.1f} nm")
print(f"  M²          = {M2:.2f}")
print(f"  lambda_eff  = {lam_eff*1e9:.1f} nm")
print(f"  MFD         = {MFD*1e6:.2f} um")
print(f"  wf          = {wf*1e6:.2f} um")
print(f"  f           = {f*1e3:.2f} mm")
print(f"  zR (Faser)  = {zR*1e3:.4f} mm")
print()
print("Bei Delta = 0 mm:")
print(f"  Strahlradius an Linse      = {w_lens[idx0]*1e3:.4f} mm")
print(f"  Strahldurchmesser an Linse = {d_lens[idx0]*1e3:.4f} mm")
print(f"  Neue Waist-Position        = {z_waist[idx0]:.4e} m")
print(f"  Neuer Waist-Radius         = {w0_new[idx0]*1e6:.4f} um")
print(f"  Neuer Waist-Durchmesser    = {d0_new[idx0]*1e6:.4f} um")
print(f"  Divergenz (Halbwinkel)     = {theta_mrad[idx0]:.4f} mrad")
print()
print("Strahlgröße hinter der Linse bei Delta = 0 mm:")
print(f"  Radius    bei 1 km   = {w_1km[idx0]:.4f} m")
print(f"  Durchmesser bei 1 km = {d_1km[idx0]:.4f} m")
print(f"  Radius    bei 500 km = {w_500km[idx0]:.4f} m")
print(f"  Durchmesser bei 500 km = {d_500km[idx0]:.4f} m")

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(5, 1, figsize=(7, 10), sharex=True)
fig.suptitle(f"Gaußstrahl-Propagation  |  M² = {M2}  |  λ = {lam*1e9:.0f} nm",
             fontsize=11)

ax[0].plot(delta*1e3, w_lens*1e3, label="Radius an der Linse")
ax[0].plot(delta*1e3, d_lens*1e3, "--", label="Durchmesser an der Linse")
ax[0].set_ylabel("Größe [mm]")
ax[0].set_title("Strahlgröße an der Linse")
ax[0].grid(True); ax[0].legend()

ax[1].plot(delta*1e3, z_waist*1e3, label="Waist-Position")
ax[1].set_ylabel("Position [mm]")
ax[1].set_title("Neue Waist-Position hinter der Linse")
ax[1].grid(True); ax[1].legend()

ax[2].plot(delta*1e3, theta_mrad, color="tab:red", label="Divergenz (Halbwinkel)")
ax[2].set_ylabel("mrad")
ax[2].set_title("Fernfeld-Divergenz")
ax[2].grid(True); ax[2].legend()

ax[3].plot(delta*1e3, w_1km, label="Radius bei 1 km")
ax[3].plot(delta*1e3, d_1km, "--", label="Durchmesser bei 1 km")
ax[3].set_ylabel("Größe [m]")
ax[3].set_title("Strahlgröße bei 1 km")
ax[3].grid(True); ax[3].legend()

ax[4].plot(delta*1e3, w_500km, label="Radius bei 500 km")
ax[4].plot(delta*1e3, d_500km, "--", label="Durchmesser bei 500 km")
ax[4].set_xlabel("Delta = s - f [mm]")
ax[4].set_ylabel("Größe [m]")
ax[4].set_title("Strahlgröße bei 500 km")
ax[4].grid(True); ax[4].legend()

plt.tight_layout()
plt.show()