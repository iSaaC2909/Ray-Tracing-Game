 # Advanced Ray-Traced Maze Game

A sophisticated 3D maze game implementing real-time ray tracing with advanced features including reflective surfaces, spheres, and dynamic lighting effects.

## Table of Contents
- [Overview](#overview)
- [Technical Architecture](#technical-architecture)
- [Game Mechanics](#game-mechanics)
- [Rendering System](#rendering-system)
- [Map Generation](#map-generation)
- [Performance Optimizations](#performance-optimizations)
- [Controls](#controls)
- [Technical Requirements](#technical-requirements)

## Overview

This game implements a first-person maze exploration experience using ray tracing for rendering. The core rendering system uses three types of rays to create realistic lighting and reflections:

1. **Vision Rays**
   - Initial rays cast from the camera
   - Determine surface intersections
   - Handle primary color calculations

2. **Reflection Rays**
   - Secondary rays for reflective surfaces
   - Support multiple bounces
   - Implement tinted reflections
   - Handle both planar and spherical reflections

3. **Shadow Rays**
   - Cast from hit points to light source
   - Calculate dynamic shadows
   - Implement soft shadow edges
   - Handle occlusion through transparent objects

## Technical Architecture

### Core Components

1. **Map System**
   - Grid-based architecture
   - Multiple feature maps:
     - Wall positions
     - Colors (RGB channels)
     - Heights
     - Reflectivity
     - Textures
     - Geometry (spheres/prisms)

2. **Rendering Pipeline**
   - Ray casting system
   - Surface intersection detection
   - Material property calculations
   - Lighting computations
   - Shadow mapping

3. **Game Logic**
   - Player movement and collision
   - Level progression
   - Win condition detection
   - Input handling

## Game Mechanics

### Level Design
- Procedurally generated mazes
- Increasing complexity with level progression
- Random wall features and properties
- Guaranteed path to exit

### Player Movement
- First-person perspective
- Collision detection with walls
- Smooth camera controls
- Height-based movement restrictions

### Objectives
- Find blue floor patch (exit)
- Navigate increasingly complex mazes
- Manage limited visibility
- Avoid getting lost in reflections

## Rendering System

### Ray Tracing Implementation

1. **Primary Ray Casting**
   ```python
   # Field of view: 60° horizontal, 45° vertical
   rot_i = rot + np.deg2rad(i/mod - 30)  # horizontal
   rot_j = rot_v + np.deg2rad(24 - j/mod)  # vertical
   ```

2. **Surface Types**
   - Regular walls
   - Reflective surfaces
   - Spheres
   - Ceiling/Floor

3. **Lighting System**
   - Dynamic light source
   - Soft shadows
   - Ambient occlusion
   - Reflection tinting

### Material Properties

1. **Walls**
   - Height variations
   - Texture mapping
   - Color properties
   - Reflectivity options

2. **Spheres**
   - Radius: 0.5 units
   - Optional reflectivity
   - Texture support
   - Transparency handling

3. **Reflective Surfaces**
   - Planar reflections
   - Spherical reflections
   - Reflection depth limit
   - Tinted reflections

## Map Generation

### Algorithm Details

1. **Initial Generation**
   ```python
   # Random feature assignment
   mapr = np.random.choice([0, 0, 0, 0, 1], (size,size))  # reflectivity
   maps = np.random.choice([0, 0, 0, 0, 1], (size,size))  # spheres
   mapt = np.random.choice([0, 0, 0, 1, 2], (size,size))  # textures
   ```

2. **Path Generation**
   - Random walker algorithm
   - Path carving
   - Exit placement
   - Wall removal

3. **Feature Distribution**
   - Edge wall enforcement
   - Feature clustering
   - Path accessibility
   - Exit visibility

## Performance Optimizations

### DDA Implementation
```python
# Digital Differential Analyzer for ray traversal
norm = np.sqrt(cos**2 + sin**2 + sinz**2)
rayDirX, rayDirY, rayDirZ = cos/norm, sin/norm, sinz/norm
```

### Key Optimizations
1. **Ray Traversal**
   - Grid-based acceleration
   - Early termination
   - Reflection depth limiting
   - Shadow ray optimization

2. **Rendering**
   - Numba JIT compilation
   - Vectorized operations
   - Resolution scaling
   - Frame skipping

3. **Memory Management**
   - Pre-allocated arrays
   - Efficient data structures
   - Minimal garbage collection
   - Cache-friendly access patterns

## Controls

### Movement
- W: Move forward
- S: Move backward
- A: Strafe left
- D: Strafe right
- Mouse: Look around

### Game Options
- ESC: Quit game
- Q: Decrease resolution
- E: Increase resolution

## Technical Requirements

### Software Dependencies
- Python 3.6+
- NumPy
- Pygame
- Numba

### Hardware Requirements
- Modern CPU (recommended)
- 4GB RAM minimum
- Graphics card supporting OpenGL 3.3+

### Performance Considerations
- Resolution impact on FPS
- Reflection depth vs performance
- Shadow quality settings
- Memory usage optimization

## Development Notes

### Code Structure
- Main game loop
- Ray tracing functions
- Map generation
- Input handling
- Rendering pipeline

### Future Improvements
- Multi-threading support
- GPU acceleration
- Advanced lighting effects
- More material types
- Level editor
