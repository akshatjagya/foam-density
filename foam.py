import streamlit as st

# Function to convert to meters
def convert_to_meters(value, unit):
    conversion_factors = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
    }
    return value * conversion_factors[unit]

# Function to calculate density
def calculate_density(mass, volume):
    return mass / volume

# Function to calculate missing dimension for cuboid
def calculate_missing_dimension(mass, density, length, breadth, height_missing):
    if height_missing:
        return mass / (density * length * breadth)
    elif length == 0:
        return mass / (density * height_missing * breadth)
    elif breadth == 0:
        return mass / (density * height_missing * length)

# Function to calculate missing thickness for cylinder
def calculate_missing_thickness(mass, density, diameter, thickness_missing):
    radius = diameter / 2
    return mass / (density * 3.14159 * (radius ** 2))

# Title
st.title("Foam Density & Dimension Calculator")

# Select shape
shape = st.selectbox("Select foam shape", ["Cuboid", "Cylinder"])

# Mass input
mass = st.number_input("Enter Mass (leave empty to calculate)", value=0.0, step=0.01)
mass_unit = st.selectbox("Mass unit", ["grams", "kilograms"])

# Density input
density = st.number_input("Enter Density (leave empty to calculate)", value=0.0, step=0.01)

if shape == "Cuboid":
    # Input dimensions for Cuboid
    length = st.number_input("Enter Length (leave empty to calculate)", value=0.0, step=0.01)
    length_unit = st.selectbox("Length unit", ["mm", "cm", "m"], key="length_unit")
    
    breadth = st.number_input("Enter Breadth (leave empty to calculate)", value=0.0, step=0.01)
    breadth_unit = st.selectbox("Breadth unit", ["mm", "cm", "m"], key="breadth_unit")
    
    height = st.number_input("Enter Thickness/Height (leave empty to calculate)", value=0.0, step=0.01)
    height_unit = st.selectbox("Height unit", ["mm", "cm", "m"], key="height_unit")

    # Convert dimensions to meters
    length_m = convert_to_meters(length, length_unit) if length > 0 else 0
    breadth_m = convert_to_meters(breadth, breadth_unit) if breadth > 0 else 0
    height_m = convert_to_meters(height, height_unit) if height > 0 else 0

    # Convert mass to kilograms if entered in grams
    if mass_unit == "grams":
        mass_kg = mass / 1000
    else:
        mass_kg = mass

    # Determine which variable to calculate
    if density > 0 and mass_kg > 0 and length_m > 0 and breadth_m > 0 and height == 0:
        # Calculate missing height
        height_m = calculate_missing_dimension(mass_kg, density, length_m, breadth_m, height_missing=True)
        height_cm = height_m * 100  # Convert back to cm for display
        st.write(f"Calculated Height: {height_cm:.2f} cm")
    elif density > 0 and mass_kg > 0 and length_m > 0 and height_m > 0 and breadth == 0:
        # Calculate missing breadth
        breadth_m = calculate_missing_dimension(mass_kg, density, length_m, breadth_m, height_missing=False)
        breadth_cm = breadth_m * 100  # Convert back to cm for display
        st.write(f"Calculated Breadth: {breadth_cm:.2f} cm")
    elif density > 0 and mass_kg > 0 and breadth_m > 0 and height_m > 0 and length == 0:
        # Calculate missing length
        length_m = calculate_missing_dimension(mass_kg, density, length_m, breadth_m, height_missing=False)
        length_cm = length_m * 100  # Convert back to cm for display
        st.write(f"Calculated Length: {length_cm:.2f} cm")
    elif density == 0:
        # Calculate density
        volume = length_m * breadth_m * height_m
        density = calculate_density(mass_kg, volume)
        st.write(f"Calculated Density: {density:.2f} kg/m³")
    elif mass == 0:
        # Calculate mass
        volume = length_m * breadth_m * height_m
        mass_kg = density * volume
        st.write(f"Calculated Mass: {mass_kg*1000:.2f} grams")

elif shape == "Cylinder":
    # Input dimensions for Cylinder
    diameter = st.number_input("Enter Diameter (leave empty to calculate)", value=0.0, step=0.01)
    diameter_unit = st.selectbox("Diameter unit", ["mm", "cm", "m"], key="diameter_unit")
    
    thickness = st.number_input("Enter Thickness (leave empty to calculate)", value=0.0, step=0.01)
    thickness_unit = st.selectbox("Thickness unit", ["mm", "cm", "m"], key="thickness_unit")

    # Convert dimensions to meters
    diameter_m = convert_to_meters(diameter, diameter_unit) if diameter > 0 else 0
    thickness_m = convert_to_meters(thickness, thickness_unit) if thickness > 0 else 0

    # Convert mass to kilograms if entered in grams
    if mass_unit == "grams":
        mass_kg = mass / 1000
    else:
        mass_kg = mass

    # Determine which variable to calculate
    if density > 0 and mass_kg > 0 and diameter_m > 0 and thickness == 0:
        # Calculate missing thickness
        thickness_m = calculate_missing_thickness(mass_kg, density, diameter_m, thickness_missing=True)
        thickness_cm = thickness_m * 100  # Convert back to cm for display
        st.write(f"Calculated Thickness: {thickness_cm:.2f} cm")
    elif density == 0:
        # Calculate density
        radius_m = diameter_m / 2
        volume = 3.14159 * (radius_m ** 2) * thickness_m
        density = calculate_density(mass_kg, volume)
        st.write(f"Calculated Density: {density:.2f} kg/m³")
    elif mass == 0:
        # Calculate mass
        radius_m = diameter_m / 2
        volume = 3.14159 * (radius_m ** 2) * thickness_m
        mass_kg = density * volume
        st.write(f"Calculated Mass: {mass_kg*1000:.2f} grams")
