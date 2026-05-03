def write_polymer_data(filename, num_monomers, bond_length=1.0):
    with open(filename, 'w') as f:
        # Header
        f.write("LAMMPS Polymer Data File\n\n")
        f.write(f"{num_monomers} atoms\n")
        f.write(f"{(9)*num_monomers//10} bonds\n\n")
        
        f.write("1 atom types\n")
        f.write("1 bond types\n\n")
        
        # Simulation Box (centered with padding)
        padding = 5.0
        max_len = (num_monomers/10) * bond_length
        f.write(f"0.0 {max_len + padding} xlo xhi\n")
        f.write(f"{-padding*5} {padding*5} ylo yhi\n")
        f.write(f"{-padding} {padding} zlo zhi\n\n")
        
        # Atoms: ID, molecule-ID, type, x, y, z
        f.write("Atoms\n\n")
        for j in range(num_monomers//10):
            y=j*padding/2.0
            for i in range(10):
                x = i * bond_length
                f.write(f"{i+1+j*10} {j+1} 1 {x:.4f} {y:4f} 0.0000\n")
            
        # Bonds: ID, type, atom1, atom2
        f.write("\nBonds\n\n")
        j=0
        for i in range(num_monomers - 1):
            if (i+1)%10==0:
                j+=1
                continue
            f.write(f"{i+1-j} 1 {i+1} {i+2}\n")

if __name__ == "__main__":
    write_polymer_data("polymers.data", num_monomers=20)
    print("File 'polymers.data' has been created.")