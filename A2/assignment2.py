import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# Constants for Argon (conversion from reduced to physical units)
# ============================================================================
sigma = 3.405e-10          # m
epsilon_kB = 119.8         # K
epsilon = epsilon_kB * 1.380649e-23  # J
N_A = 6.02214076e23        # mol^-1

def p_star_to_bar(p_star):
    """Convert reduced pressure to bar"""
    return p_star * epsilon / (sigma**3) / 1e5

def u_star_to_kJmol(u_star):
    """Convert reduced energy per particle to kJ/mol"""
    return u_star * epsilon * N_A / 1000

def read_amclj_results(filename="amclj.log"):
    U_star = None
    p_star = None

    with open(filename, "r") as f:
        for line in f:
            if "<U>/N" in line:
                U_star = float(line.split('=')[1].strip())
            elif line.strip().startswith("p="):
                p_star = float(line.split('=')[1].strip())

    if U_star is None or p_star is None:
        raise ValueError("Could not parse amclj output. Check file format.")

    return U_star, p_star
def read_amclj_results(filename="amclj.log"):
    import re

    U_star = None
    p_star = None

    with open(filename, "r") as f:
        for line in f:
            if "<U>/N" in line:
                U_star = float(re.findall(r"[-+]?\d+\.\d+e[+-]\d+", line)[0])
            elif line.strip().startswith("p="):
                p_star = float(re.findall(r"[-+]?\d+\.\d+e[+-]\d+", line)[0])

    if U_star is None or p_star is None:
        raise ValueError("Could not parse amclj output. Check file content.")

    return U_star, p_star
# Experimental values
U_exp = -5.97  # kJ/mol
P_exp = 0.689  # bar

# Read simulation data
data = np.loadtxt('log.dat', skiprows=1)  # Skip header if present
steps = data[:, 0]
energy_star = data[:, 2]
pressure_star = data[:, 3]


# Read correct ensemble averages from amclj
U_star_mean, P_star_mean = read_amclj_results("amclj.log")

# Convert to physical units
U_physical = u_star_to_kJmol(U_star_mean)
P_physical = p_star_to_bar(P_star_mean)

## Calculate averages
#U_star_mean = np.mean(energy_star)
#P_star_mean = np.mean(pressure_star)
#
## Convert to physical units
#U_physical = u_star_to_kJmol(U_star_mean)
#P_physical = p_star_to_bar(P_star_mean)

# Print results
print("="*50)
print("SIMULATION RESULTS")
print("="*50)
print(f"\nReduced units:")
print(f"  ⟨U*⟩ = {U_star_mean:.4f} ε/particle")
print(f"  ⟨p*⟩ = {P_star_mean:.6f} ε/σ³")
print(f"\nPhysical units:")
print(f"  ⟨U⟩ = {U_physical:.3f} kJ/mol")
print(f"  ⟨p⟩ = {P_physical:.4f} bar")
print(f"\nExperimental values:")
print(f"  U_exp = {U_exp:.2f} kJ/mol")
print(f"  P_exp = {P_exp:.3f} bar")
print(f"\nDifferences:")
print(f"  ΔU = {(U_physical - U_exp)/abs(U_exp)*100:.1f}%")
print(f"  ΔP = {(P_physical - P_exp)/P_exp*100:.1f}%")

# Plot convergence
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Energy convergence
ax1.plot(steps, energy_star, 'b-', linewidth=0.5, alpha=0.7)
ax1.axhline(y=U_star_mean, color='r', linestyle='--', 
            label=f'Mean: {U_star_mean:.4f}')

ax1.set_xlabel('MC Steps')
ax1.set_ylabel('Energy (ε)')
ax1.set_title('Energy Convergence')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Pressure convergence
ax2.plot(steps, pressure_star, 'r-', linewidth=0.5, alpha=0.7)
ax2.axhline(y=P_star_mean, color='b', linestyle='--', 
            label=f'Mean: {P_star_mean:.6f}')
ax2.set_xlabel('MC Steps')
ax2.set_ylabel('Pressure (ε/σ³)')
ax2.set_title('Pressure Convergence')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('convergence.png', dpi=150)
plt.show()

# Plot g(r) 
try:
    gr_data = np.loadtxt('amclj.dat')
    r = gr_data[:, 0]
    g_r = gr_data[:, 1]
    
    plt.figure(figsize=(10, 6))
    plt.plot(r, g_r, 'b-', linewidth=2)
    plt.xlabel('r (σ)')
    plt.ylabel('g(r)')
    plt.title('Radial Distribution Function')
    plt.grid(True, alpha=0.3)
    plt.savefig('gr.png', dpi=150)
    plt.show()
    print("\n g(r) plot saved as gr.png")
except:
    print("\n  No amclj.dat found")