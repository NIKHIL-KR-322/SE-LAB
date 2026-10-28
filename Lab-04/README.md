# Fruit Catcher Repair Lab

A 2D arcade-style Fruit Catcher game developed using **Python and Pygame**.

The project was provided as a working game containing one deliberate bug and three optional enhancement tasks. The game was analyzed, repaired, tested, and enhanced using an LLM as a debugging and pair-programming assistant.

---

## Project Overview

The player controls a basket at the bottom of the screen and attempts to catch falling fruits.

### Normal Fruits

The game contains:

* Apple
* Orange
* Grape

Successfully catching a normal fruit increases the score by **1**.

### Hazard Fruit

A hazard item occasionally appears instead of a normal fruit.

The hazard is displayed as a dark/black object with green markings.

Catching a hazard deducts **1 life** and does not increase the score.

---

## Features

* Basket movement using keyboard controls
* `A` / `D` keyboard controls
* Left / Right arrow controls
* Random fruit spawning
* Random fruit falling speeds
* Score tracking
* Three-life system
* Game Over state
* Restart functionality
* Hazard fruits
* Dynamic difficulty progression
* Increasing fruit falling speed
* Decreasing fruit spawn delay
* Fruit splash particle effects

---

# Tasks Completed

## Task 1 — Fix Floor Miss Scoring and Life Deduction

### Original Problem

When a fruit reached the bottom of the screen, the original code incorrectly executed:

```python
self.score += 1
```

This caused the score to increase even when the player missed a fruit.

The original game also did not correctly deduct lives when a fruit was missed.

### Modification

The miss logic was changed so that a missed fruit:

* Decreases the player's lives by 1.
* Does not increase the score.
* Is removed from the active fruit list.
* Changes the game state to `GAME_OVER` when lives reach 0.

### Result

```text
Catch fruit → Score +1

Miss fruit → Life -1
```

---

# Task 2 — Rotten Fruit / Hazard Bomb

A hazard item was added to the `Fruit` class.

The hazard is randomly generated with a probability of approximately **15%**.

Normal fruits retain their original colors, while hazards are displayed differently so that the player can identify and avoid them.

### Hazard Behavior

When a hazard collides with the basket:

```text
Lives -1
Score unchanged
```

If all lives are lost:

```text
GAME_OVER
```

This introduces a dodge mechanic to the game.

---

# Task 3 — Dynamic Falling Speed Escalation

The game difficulty now increases as the player's score increases.

The speed bonus is calculated based on the current score:

```python
speed_bonus = min(self.score * 0.15, 3.0)
```

The spawn delay is also reduced as the score increases:

```python
self.spawn_delay = max(
    300,
    750 - self.score * 15
)
```

Therefore:

```text
Score increases
       ↓
Fruit speed increases
       ↓
Spawn delay decreases
       ↓
More challenging gameplay
```

A maximum speed bonus and minimum spawn delay are used to prevent the game from becoming excessively fast.

---

# Task 4 — Fruit Splash Particle Effects

A lightweight particle system was added to the game engine.

When a normal fruit is caught or reaches the floor, small colored particles are generated.

Each particle has:

* Position
* Horizontal velocity
* Vertical velocity
* Lifetime
* Fruit color

Particles are updated every frame and removed after their lifetime expires.

A small gravity effect is also applied to make the particles move naturally.

### Particle Flow

```text
Fruit caught / missed
        ↓
Create particles
        ↓
Particles move outward
        ↓
Gravity affects particles
        ↓
Particles disappear
```

The particle color matches the fruit that generated the splash.

---

# Game Controls

| Key | Action                  |
| --- | ----------------------- |
| `A` | Move basket left        |
| `D` | Move basket right       |
| `←` | Move basket left        |
| `→` | Move basket right       |
| `R` | Restart after Game Over |

---

# Game Rules

### Catching a Normal Fruit

```text
Normal fruit + Basket
        ↓
Score +1
        ↓
Fruit removed
        ↓
Particle effect
```

### Missing a Fruit

```text
Fruit reaches floor
        ↓
Lives -1
        ↓
Fruit removed
        ↓
Particle effect
```

### Catching a Hazard

```text
Hazard + Basket
        ↓
Lives -1
        ↓
Score unchanged
        ↓
Hazard removed
```

### Losing All Lives

```text
Lives = 0
    ↓
GAME OVER
    ↓
Game updates stop
    ↓
Press R to restart
```

---

# Restart Behavior

After Game Over, pressing `R` resets:

```text
Score → 0
Lives → 3
Fruits → Cleared
Particles → Cleared
Game State → PLAYING
```

---

# Installation

## Requirements

* Python 3.10 or later
* Pygame

Install Pygame:

```bash
pip install pygame
```

---

# Running the Game

Open a terminal in the project directory:

```bash
python main.py
```

If Python is installed but `python` is not available in PATH, the Python executable can also be used directly.

---

# Project Structure

```text
Fruit-catcher/
│
├── game/
│   ├── basket.py
│   ├── fruit.py
│   └── game_engine.py
│
├── main.py
├── README.md
└── DELIVERABLES.md
```

---

# Testing

The game was executed locally and tested during gameplay.

The following were verified:

* Normal fruit catching
* Score increase after successful catches
* Life deduction after missed fruits
* Hazard fruit behavior
* Hazard life deduction
* Game Over behavior
* Restart functionality
* Dynamic fruit speed
* Dynamic spawn delay
* Particle splash effects

---

# Submission Deliverables

The submission consists of:

1. **Before-change gameplay video** — approximately 10 seconds.
2. **After-change gameplay video** — approximately 10 seconds.
3. **LLM / Chat history link** showing the development and debugging process.
LLM LINK:  https://chatgpt.com/share/6abd0719-1920-83ee-b433-f31a09cb2420

---

# Repository

Student repository:

`NIKHIL-KR-322/Fruit-catcher`

The original source repository was used as the starting point, while the completed work was maintained in the student's separate repository.
