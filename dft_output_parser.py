import re
import numpy as np

def parse_gaussian_dft_energy(log_file_lines):
    """
    Parses SCF Done electronic energy and HOMO-LUMO gap from Gaussian/ORCA 
    DFT output logs for Furan & 1,10-Phenanthroline transition metal complexes.
    """
    scf_energies = []
    homo_energy = None
    lumo_energy = None
    
    for line in log_file_lines:
        if "SCF Done:" in line:
            match = re.search(r"SCF Done:\s+E\([A-Za-z0-9]+\)\s+=\s+([-0-9.]+)", line)
            if match:
                scf_energies.append(float(match.group(1)))
                
        if "Alpha  occ. eigenvalues --" in line:
            vals = [float(x) for x in line.split("--")[1].split()]
            homo_energy = vals[-1]
            
        if "Alpha virt. eigenvalues --" in line and lumo_energy is None:
            vals = [float(x) for x in line.split("--")[1].split()]
            lumo_energy = vals[0]

    if not scf_energies:
        return None

    final_energy_hartree = scf_energies[-1]
    final_energy_kcal = final_energy_hartree * 627.509474
    
    homo_lumo_gap_ev = None
    if homo_energy is not None and lumo_energy is not None:
        homo_lumo_gap_ev = (lumo_energy - homo_energy) * 27.2114

    return {
        "final_scf_hartree": round(final_energy_hartree, 6),
        "final_scf_kcal_mol": round(final_energy_kcal, 2),
        "homo_lumo_gap_ev": round(homo_lumo_gap_ev, 4) if homo_lumo_gap_ev else None
    }

if __name__ == "__main__":
    sample_log = [
        " SCF Done:  E(RB3LYP) =  -1452.389412     A.U. after   14 cycles",
        " Alpha  occ. eigenvalues --  -0.31240  -0.28910  -0.21450",
        " Alpha virt. eigenvalues --  -0.08120  -0.04510   0.01230"
    ]
    print("DFT Complex Analysis:", parse_gaussian_dft_energy(sample_log))
