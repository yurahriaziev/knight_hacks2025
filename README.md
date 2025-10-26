# Visigen  
**From Words to Worlds — Turning Physics Problems into Interactive 3D Simulations**

---

## Inspiration  

Physics problems are often described in words — but truly understanding them requires visualization.  
When we read something like:

> “A 5 kg sphere rolls down a 30° incline without friction.”

we’re forced to *imagine* what’s happening: the slope, the motion, the forces involved.  

That gap between **text and visualization** inspired us to create **Visigen** — a system that converts written word problems into **interactive 3D physics simulations**.  
We wanted to make learning **intuitive, immersive, and visual**, so students can *see* physics come to life.

---

## What it does  

Visigen allows users to input any **physics word problem**, and within seconds, it:

1. **Parses** the natural language description to extract key parameters like mass, friction, and angle.  
2. **Generates** a structured 3D scene (in JSON format) describing objects, environment, and simulation properties.  
3. **Validates** and refines the scene through an AI agent feedback loop.  
4. **Renders** the simulation in real-time using **React Three Fiber** and **Rapier Physics**.  

Students can instantly visualize motion, friction, and forces — making complex formulas tangible.

$$
a = g(\sin{\theta} - \mu \cos{\theta})
$$

---

## How we built it  

**Frontend:**  
- Built with **React + Vite** and styled with **Tailwind CSS**  
- Used **React Three Fiber** for 3D rendering  
- Integrated **Rapier Physics** for realistic motion, collisions, and friction  
- Added **Lottie animations** for dynamic and themed loading visuals  

**Backend (FastAPI):**  
- Developed an **AI Agent System**:
  - `parser_agent` — understands natural language problems and extracts data  
  - `scene_agent` — creates 3D environment blueprints in structured JSON  
  - `validator_agent` — checks and refines simulation parameters  
  - `a2a_manager` — orchestrates the full autonomous “parser → builder → validator” pipeline  
- Supports mathematical reasoning for motion, friction, and gravity using physical equations:  

$$
F = ma, \quad \mu = \frac{f}{N}, \quad a = g \sin{\theta}
$$

- Connected to the frontend via **CORS-enabled FastAPI endpoints**

---

## Challenges we ran into  

- **Understanding Natural Language:** Translating text like “slides without friction” vs “rolls down” into meaningful physics parameters  
- **Scene Construction:** Ensuring the incline, objects, and base aligned perfectly in 3D space without clipping or floating issues  
- **Realistic Physics Tuning:** Balancing Rapier’s parameters for realistic acceleration, restitution, and motion  
- **Camera Composition:** Creating a fixed but cinematic view that works for all simulations  

---

## Accomplishments that we're proud of  

- Built a complete **AI-to-Simulation pipeline** from scratch within a short time frame  
- Achieved **fully dynamic 3D rendering** directly from natural language  
- Designed an elegant **UI/UX** that feels both educational and futuristic  
- Demonstrated **autonomous agent collaboration** between parsing, validation, and visualization  

---

## What we learned  

- How to merge **language models**, **mathematical reasoning**, and **3D physics** into one cohesive system  
- The power of **AI-driven interpretation** in education — bridging human text with computational understanding  
- That visual feedback is one of the fastest ways to reinforce conceptual learning  
- How to debug physics simulations that don’t always behave as expected (yes, we lost a few spheres through the floor)  

---

## What's next for Visigen  

- Support more complex scenarios — projectiles, pendulums, pulleys, and rotational dynamics  
- Display **live equations and numeric outputs** alongside simulations  
- Enable **adjustable sliders** for mass, friction, and angles (coming soon)  
- Deploy to **AWS EC2** with a public demo and a shared model inference endpoint  
- Partner with educators to integrate Visigen into interactive learning platforms  

---
