import math

def degree_to_ft_per_ft(degree_slope):
    # Convert degrees to radians
    radians = math.radians(degree_slope)
    # Calculate ft/ft slope
    slope_ft_per_ft = math.tan(radians)
    return slope_ft_per_ft


degree_slope = 6
ft_per_ft_slope = degree_to_ft_per_ft(degree_slope)
print(f"Slope in ft/ft: {ft_per_ft_slope}")
