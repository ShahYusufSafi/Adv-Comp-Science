import numpy as np
import matplotlib.pyplot as plt

# Experimental values in reduced units
# From earlier calculation
U_star_exp = -5.9935  # ε/particle
P_star_exp = 0.001644  # ε/σ³

# Read production run log
try:
    data = np.loadtxt('log_prod.dat')
    steps = data[:, 0]
    energy_star = data[:, 2]
    pressure_star = data[:, 3]
    
    # Calculate averages (no need to discard since zmclj reset)
    U_star_mean = np.mean(energy_star)
    U_star_std = np.std(energy_star)
    P_star_mean = np.mean(pressure_star)
    P_star_std = np.std(pressure_star)
    
    print("="*60)
    print("ARGON TRIPLE POINT SIMULATION RESULTS")
    print("="*60)
    print(f"\nSimulation details:")
    print(f"  Total steps: {len(steps)}")
    print(f"  Acceptance rate: {np.mean(data[:,1]):.3f}")
    
    print(f"\nPotential Energy (reduced units):")
    print(f"  ⟨U*⟩ = {U_star_mean:.4f} ± {U_star_std/np.sqrt(len(energy_star)):.4f} ε")
    print(f"  Expected: {U_star_exp:.4f} ε")
    print(f"  Difference: {(U_star_mean - U_star_exp)/abs(U_star_exp)*100:.1f}%")
    
    print(f"\nPotential Energy (physical):")
    print(f"  ⟨U⟩ = {U_star_mean * 0.996:.3f} kJ/mol")
    print(f"  Expected: -5.97 kJ/mol")
    
    print(f"\nPressure (reduced units):")
    print(f"  ⟨p*⟩ = {P_star_mean:.6f} ± {P_star_std/np.sqrt(len(pressure_star)):.6f}")
    print(f"  Expected: {P_star_exp:.6f}")
    print(f"  Difference: {(P_star_mean - P_star_exp)/P_star_exp*100:.1f}%")
    
    print(f"\nPressure (physical):")
    print(f"  ⟨p⟩ = {P_star_mean * 419:.2f} bar")
    print(f"  Expected: 0.689 bar")
    
    # Plot convergence
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(steps, energy_star, 'b-', linewidth=0.5)
    ax1.axhline(y=U_star_mean, color='r', linestyle='--', 
                label=f'Mean: {U_star_mean:.4f}')
    ax1.axhline(y=U_star_exp, color='g', linestyle=':', 
                label=f'Expected: {U_star_exp:.4f}')
    ax1.set_xlabel('MC Steps')
    ax1.set_ylabel('Energy (ε)')
    ax1.set_title('Energy Convergence')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(steps, pressure_star, 'r-', linewidth=0.5)
    ax2.axhline(y=P_star_mean, color='b', linestyle='--', 
                label=f'Mean: {P_star_mean:.6f}')
    ax2.axhline(y=P_star_exp, color='g', linestyle=':', 
                label=f'Expected: {P_star_exp:.6f}')
    ax2.set_xlabel('MC Steps')
    ax2.set_ylabel('Pressure (ε/σ³)')
    ax2.set_title('Pressure Convergence')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('convergence.png')
    plt.show()
    
except FileNotFoundError:
    print("log_prod.dat not found!")
    print("Make sure you ran the production simulation first.")