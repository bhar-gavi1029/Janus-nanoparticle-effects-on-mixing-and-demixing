import numpy as np
def write_polymer_data(filename, num_bead,per_chain=20, bond_length=0.3,jr=1):
    

    def calculate_n_for_radius(radius, density_factor=10):
        """
        radius: The radius of your sphere
        density_factor: Points per unit of surface area
        """
        surface_area = 4 * np.pi * (radius**2)
        return int(surface_area * density_factor)

    n_points = calculate_n_for_radius(jr)
    num_monomers=num_bead-2*n_points

    with open(filename, 'w') as f:
        # Header
        f.write("LAMMPS Polymer Data File\n\n")
        f.write(f"{num_bead} atoms\n")
        f.write(f"{(per_chain-1)*num_monomers//per_chain} bonds\n")
        f.write(f"{(per_chain-2)*num_monomers//per_chain} angles\n\n")
        
        f.write("4 atom types\n")
        f.write("1 bond types\n")
        f.write("1 angle types\n\n")
        
        # Simulation Box (centered with padding)
        per_type=num_monomers//(2*per_chain)
        padding = 1.5
        max_len = 12.0 -padding
        f.write(f"0.0 {max_len+padding} xlo xhi\n")
        f.write(f"0.0 {max_len+padding} ylo yhi\n")
        f.write(f"0.0 {max_len+padding} zlo zhi\n\n")
        
        # Atoms: ID, molecule-ID, type, x, y, z
        f.write("Atoms\n\n")
        b,dx,dy,i=1,1,1,0 #d is direction 1 right -1 for left
        x,y,z=padding,padding,padding
        while(b<=num_monomers):
            t=((b-1)//per_chain)+1 
            x+=(dx)*bond_length

            if x>max_len or x<=padding:
                y+=(dy)*bond_length
                if y>max_len or y<=padding:
                    z+=bond_length
                    y-=(dy)*bond_length
                    dy*=-1
                x-=(dx)*bond_length
                dx*=-1

            f.write(f"{b} {t} {((t-1)//per_type) +1 } {x:.4f} {y:4f} {z:4f}\n")
            b+=1
              
        #janus particle
        """Generates evenly distributed points on a sphere."""
        # Atoms: ID, molecule-ID, type, x, y, z
        # Golden angle in radians
        phi = np.pi * (3. - np.sqrt(5.))
        cx,cy,cz=padding+1,padding+1,z+1.5
        for n in range(2):

            for i in range(n_points):
                y =1 - (i / float(n_points - 1)) * 2  # y goes from -1 to 1
                radius = np.sqrt(1 - y * y)  # radius at y

                theta = phi * i  # golden angle increment

                x = np.cos(theta) * radius
                z = np.sin(theta) * radius
                f.write(f"{b} {t+1} {3 if theta%(2*np.pi)<np.pi else 4} {jr*(x+cx):.4f} {jr*(y+cy):4f} {jr*(z+cz):4f}\n")
                b+=1    
            cy+=2*jr+bond_length  
            t+=1 

            
        # Bonds: ID, type, atom1, atom2
        f.write("\nBonds\n\n")
        j=0
        for i in range(num_monomers - 1):
            if (i+1)%per_chain==0 and i!=0:
                j+=1
                continue

            f.write(f"{i+1-j} 1 {i+1} {i+2}\n")

        


        # Angles: ID, type, atom1, atom2, atom3
        f.write("\nAngles\n\n")
        j=0
        for i in range(num_monomers - 2):
            if (i+2)%per_chain==0 or (i+1)%per_chain==0 and i!=0:
                j+=1
                continue

            f.write(f"{i+1-j} 1 {i+1} {i+2} {i+3}\n")
         


        

if __name__ == "__main__":
    write_polymer_data("polymer_chain_multiple_3_jr1_2.data", num_bead=5180,per_chain=10,jr=1)
    print("File 'polymer_chain_multiple_3_jr1_2.data' has been created.")