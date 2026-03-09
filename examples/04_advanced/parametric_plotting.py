"""
Advanced: Parametric Surface Plotting

Create 3D parametric plots for mathematical visualization.
Demonstrates: Mesh3d + mathematical functions + custom coloring
"""
import numpy as np
import plotly.graph_objects as go

# Define parametric equations for a 3D surface (Möbius strip)
def mobius_strip(u, v, R=2):
    """
    Parametric equations for Möbius strip
    u: [0, 2π] - angle around the strip
    v: [-1, 1] - position along the width
    R: radius
    """
    x = (R + v * np.cos(u/2)) * np.cos(u)
    y = (R + v * np.cos(u/2)) * np.sin(u)
    z = v * np.sin(u/2)
    return x, y, z

# Generate parametric surface
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(-0.5, 0.5, 20)
U, V = np.meshgrid(u, v)

X, Y, Z = mobius_strip(U, V)

# Create 3D surface plot
fig = go.Figure(data=[
    go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Height'),
        lighting=dict(
            ambient=0.4,
            diffuse=0.8,
            roughness=0.5,
            specular=0.6,
            fresnel=0.2
        ),
        lightposition=dict(x=100, y=200, z=0)
    )
])

# Update layout for 3D
fig.update_layout(
    title='Möbius Strip - Parametric Surface',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2)
        ),
        aspectmode='cube'
    ),
    width=800,
    height=800
)

print("🎲 Displaying 3D parametric surface (Möbius strip)...")
print("Drag to rotate, scroll to zoom")
fig.show()

# Bonus: Create a second example - torus
def torus(theta, phi, R=3, r=1):
    """
    Parametric equations for torus
    theta, phi: [0, 2π] angles
    R: major radius, r: minor radius
    """
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# Generate torus
theta = np.linspace(0, 2*np.pi, 100)
phi = np.linspace(0, 2*np.pi, 50)
THETA, PHI = np.meshgrid(theta, phi)
X_t, Y_t, Z_t = torus(THETA, PHI)

fig2 = go.Figure(data=[
    go.Surface(x=X_t, y=Y_t, z=Z_t, colorscale='Portland')
])

fig2.update_layout(
    title='Torus - Parametric Surface',
    scene=dict(
        aspectmode='data',
        camera=dict(eye=dict(x=1.3, y=1.3, z=1.3))
    ),
    width=700,
    height=700
)

print("\n🍩 Displaying torus surface...")
fig2.show()
