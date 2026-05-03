def convert_lammps_data_to_xyz(data_file, xyz_file):
    with open(data_file, 'r') as f:
        lines = f.readlines()

    # Find the number of atoms
    num_atoms = 0
    for line in lines:
        if 'atoms' in line:
            num_atoms = int(line.split()[0])
            break

    # Find the Atoms section
    atoms_start = -1
    for i, line in enumerate(lines):
        if line.strip() == 'Atoms':
            atoms_start = i + 2  # Skip 'Atoms' and the empty line
            break

    if atoms_start == -1 or num_atoms == 0:
        print("Could not find Atoms section or number of atoms.")
        return

    # Extract atoms
    atoms = []
    for i in range(atoms_start, atoms_start + num_atoms):
        parts = lines[i].split()
        if len(parts) >= 6:
            # For this specific data format: atom-ID molecule-ID atom-type x y z
            # (or atom-ID atom-type x y z if missing molecule-ID, but we assume parts[2] is type, 3,4,5 are coords based on your file)
            # Standard molecular format is: atom-ID molecule-ID atom-type x y z
            # VMD XYZ format needs: element x y z (we'll use atom-type as element)
            atom_type = parts[2]
            x = parts[3]
            y = parts[4]
            z = parts[5]
            atoms.append(f"{atom_type} {x} {y} {z}\n")

    # Write to XYZ file
    with open(xyz_file, 'w') as f:
        f.write(f"{num_atoms}\n")
        f.write(f"Generated from {data_file}\n")
        for atom in atoms:
            f.write(atom)

if __name__ == "__main__":
    convert_lammps_data_to_xyz('polymers.data', 'polymers.xyz')
    print("Conversion complete: polymers.xyz created.")
