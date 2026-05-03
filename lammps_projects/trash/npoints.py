import numpy as np
def calculate_n_for_radius(radius, density_factor=10):
        """
        radius: The radius of your sphere
        density_factor: Points per unit of surface area
        """
        surface_area = 4 * np.pi * (radius**2)
        return int(surface_area * density_factor)
n_points=calculate_n_for_radius(1)
print(n_points)