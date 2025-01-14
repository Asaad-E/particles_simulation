# Particle Simulation

<img src="https://github.com/Asaad-E/particles_simulation/blob/master/media/video.gif" width="500" height="375"/>

This is a  2D particle collision simulator that allows you to interact with particles in multiple containers. You can drag existing particles, create new ones, zoom in/out, and scroll through the containers.

## Collisions

The simulator uses the two-dimensional elastic collision formula for particle interactions, as described on [Wikipedia](https://en.wikipedia.org/wiki/Elastic_collision).

## Controls

- **Zoom in:** Press the 'Z' key
- **Zoom out:** Press the 'X' key
- **Reset Zoom**: Press the 'R' key
- **Drag a particle:** Left-click on the particle
- **Move the window:** Right-click and drag
- **Add a particle:** Center-click (middle mouse button)

## Dependencies

- Python 3
- Pygame (>= 2.6.1)

## Running the Simulation

1. Clone the repository.

```bash
git clone https://github.com/Asaad-E/particles_simulation.git
```

2. Move to the project folder.

```bash
cd ./particles_simulation

```

3. Install the required dependencies:

```bash
    pip install -r requirements.tx
```

4. Execute main script:

```bash
python ./particles_simulation/main.py
```

## **Simulation parameters**

You can modify various simulation parameters directly in the main.py file. These parameters include:

- **Mouse strength:** This affects the force applied to particles when dragging them.
- **Screen size:** This defines the width and height of each container.
  Number of environments: This specifies the number of containers to simulate.
- **Particle limits:** Set the minimum and maximum number of particles allowed per container.
- **Particles per environment:** Define the initial number of particles in each container.
- **Zoom level:** Control the zoom applied to the simulation.
- **Particle addition delay:** This sets the time delay between adding new particles.
