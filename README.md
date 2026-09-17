# Disaster Response Training Game

An interactive disaster response training game developed using **Python and Pygame**. The project uses a story-based simulation to present an emergency situation and allows the player to make decisions that lead to different outcomes.

The current prototype focuses on an **earthquake response scenario in a classroom environment**, combining interactive storytelling, visual scenes, audio narration, sound effects, animations, and decision-based gameplay.

---

## Project Overview

Disaster preparedness is often taught through theoretical instructions, but interactive simulations can provide a more engaging way to understand emergency-response situations.

This project was developed as an educational game prototype that demonstrates how disaster-response training can be presented through an interactive story.

The player follows a group of students through a classroom scenario. When an earthquake occurs, the player reaches a decision point and must choose how to respond. The selected action determines the outcome of the simulation.

The project combines:

- Interactive storytelling
- Disaster-response simulation
- Decision-based gameplay
- Audio narration
- Sound effects
- Visual scenes
- Animated transitions
- Interactive user interface
- Game-state management

---

## Objectives

The main objectives of the project are:

1. To demonstrate disaster-response awareness through interactive gameplay.
2. To present emergency situations using a story-based simulation.
3. To provide decision-based interactions with different outcomes.
4. To integrate audio, visual scenes, and animation into an educational application.
5. To demonstrate the use of Python and Pygame for interactive software development.

---

## Key Features

### Interactive Storytelling

The game presents a sequence of story scenes involving students in a classroom environment.

### Earthquake Scenario

The current implemented scenario simulates an earthquake occurring during a classroom session.

### Decision-Based Gameplay

At the critical stage of the simulation, the player is presented with two choices:

- Run Outside
- Hide Under Bench

The selected choice determines the resulting outcome.

### Multiple Outcomes

The game provides separate success and failure outcomes depending on the selected action.

### Audio Narration

Individual story events use voice recordings to provide narration and dialogue.

### Sound Effects

The application includes sound effects for:

- Button clicks
- Earthquake events
- Successful outcomes
- Failed outcomes

### Animated Text

Story dialogue is displayed using animated text rather than displaying the entire message at once.

### Scene Transitions

The application includes fade-in transitions and animated subtitle movement between scenes.

### Earthquake Screen Shake

During earthquake-related scenes, the screen uses a dynamic shake effect to create a stronger simulation experience.

### Interactive Menus

The application includes:

- Main menu
- Mode selection
- Level selection
- Gameplay screen
- Success outcome screen
- Failure outcome screen

### Game Navigation

Users can navigate between different screens using buttons and keyboard input.

---

## Gameplay Flow

The current prototype follows this sequence:

```text
Main Menu
    │
    ▼
Select Mode
    │
    ▼
Select Level
    │
    ▼
Students leave home
    │
    ▼
Students arrive at school
    │
    ▼
Classroom scene
    │
    ▼
Teacher enters
    │
    ▼
Lesson begins
    │
    ▼
Teacher receives a phone call
    │
    ▼
Teacher leaves the classroom
    │
    ▼
Earthquake begins
    │
    ▼
Students panic
    │
    ▼
Player Decision
   / \
  /   \
 ▼     ▼
Run    Hide Under
Outside Bench
  │      │
  ▼      ▼
Failure Success
```

---

## Technologies Used

### Programming Language

- Python

### Framework / Library

- Pygame

### Development Concepts

- Event-driven programming
- Game-state management
- Interactive simulation
- Game logic
- User interaction
- Audio integration
- UI development
- Animation
- Scene management

---

## Project Architecture

The application is organized around different game states and story scenes.

### Main Game States

The program includes the following major states:

```text
menu
mode_select
level_select
game
```

These states control which screen or stage is displayed to the user.

### Story States

The story is represented using separate scenes such as:

```text
start_journey
class_entry
teacher_entry
teaching
teacher_call
earthquake_start
panic_scene
decision
bad_ending
good_ending
```

Each scene can contain:

- Dialogue
- Voice audio
- Background image
- Next scene
- User choices

---

## Game Features in Detail

### Story System

The project uses a structured story dictionary containing scene information.

Each story scene can define:

- Text
- Voice file
- Image file
- Next scene
- Decision choices

This allows the gameplay sequence to be controlled through the story data.

### Audio System

The application loads sound effects and voice recordings from the `assets/sounds` directory.

The project uses audio for:

- Dialogue narration
- Button feedback
- Earthquake effects
- Success notification
- Failure notification

### Animation System

The project includes several visual animation effects:

- Animated dialogue text
- Fade-in scene transitions
- Subtitle slide-in animation
- Hover effects
- Button pulse animation
- Earthquake screen shake

### User Interface

The user interface contains:

- Main menu buttons
- Mode selection buttons
- Level selection grid
- Back buttons
- Next button
- Decision buttons
- Outcome buttons

---

## Current Game Scenario

The current implemented scenario begins with students leaving home and travelling to school.

The story then progresses through the classroom environment:

1. Students arrive at school.
2. Students enter the classroom.
3. The teacher enters.
4. The lesson begins.
5. The teacher receives a phone call.
6. The teacher leaves the classroom.
7. An earthquake suddenly occurs.
8. Students panic.
9. The player must make a decision.
10. The selected decision leads to either the failure or success outcome.

---

## Decision System

At the decision stage, the player receives two options:

### Option 1 — Run Outside

This leads to the failure outcome in the current prototype.

The scene explains that students rush outside during the earthquake and may be injured by falling objects.

### Option 2 — Hide Under Bench

This leads to the success outcome in the current prototype.

The scene presents students taking shelter under desks during the earthquake.

---

## Success and Failure Screens

### Success Outcome

The success screen displays:

```text
LEVEL COMPLETED!
Drop, Cover, Hold – You saved everyone!
```

### Failure Outcome

The failure screen displays:

```text
LEVEL FAILED
Running during an earthquake is dangerous!
```

The user can then return to the menu or retry the scenario where supported.

---

## Level and Mode System

The current interface includes three modes:

```text
Easy
Medium
Hard
```

The level-selection interface is also designed for multiple levels.

The current prototype has the first Easy level unlocked while the remaining levels are currently locked in the implementation.

This structure provides a base for expanding the application with additional disaster scenarios and training levels.

---

## Project Structure

```text
Disaster-Response-Training-Python-Pygame/
│
├── README.md
├── disaster_response.py
├── requirements.txt
│
└── assets/
    │
    ├── menu.png
    ├── classroom.png
    │
    ├── scenes/
    │   ├── start_journey.png
    │   ├── class_entry.png
    │   ├── teacher_entry_1.png
    │   ├── teacher_entry_3.png
    │   ├── teaching.png
    │   ├── teacher_call_1.png
    │   ├── teacher_call_2.png
    │   ├── earthquake_start_1.png
    │   ├── earthquake_start_2.png
    │   ├── panic.png
    │   ├── bad_ending.png
    │   └── good_ending.png
    │
    └── sounds/
        ├── click.wav
        ├── earthquake.wav
        ├── fail.wav
        ├── success.wav
        ├── bad_ending.mp3
        ├── good_ending.mp3
        │
        └── voices/
            ├── start_journey.mp3
            ├── class_entry.mp3
            ├── teacher_entry_1.mp3
            ├── teacher_entry_2.mp3
            ├── teaching.mp3
            ├── teacher_call_1.mp3
            ├── teacher_call_2.mp3
            ├── earthquake_start.mp3
            ├── panic_1.mp3
            ├── panic_2.mp3
            ├── decision.mp3
            ├── run_away.mp3
            ├── bad_ending.mp3
            ├── hide_under.mp3
            └── good_ending.mp3
```

> The exact asset files may be expanded or modified as additional scenarios and levels are developed.

---

## Requirements

The project currently requires:

```text
pygame
```

The dependency is listed in:

```text
requirements.txt
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MdThoufeeq/Disaster-Response-Training-Python-Pygame.git
```

### 2. Open the Project Directory

```bash
cd Disaster-Response-Training-Python-Pygame
```

### 3. Install the Required Package

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run:

```bash
python disaster_response.py
```

The application will open the main game window.

---

## Important Note About Assets

The program loads images and audio files using relative paths such as:

```text
assets/sounds/click.wav
assets/sounds/earthquake.wav
assets/sounds/bad_ending.mp3
assets/sounds/good_ending.mp3
assets/scenes/start_journey.png
```

Therefore, the `assets` directory must remain in the correct location relative to `disaster_response.py`.

Do not move or rename asset files unless the corresponding paths in the Python program are also updated.

---

## Controls

The application primarily uses the mouse for interaction.

### Mouse

Used for:

- Menu selection
- Mode selection
- Level selection
- Decision selection
- Next button
- Retry
- Menu navigation

### Keyboard

During gameplay, a key press can advance the story to the next scene when the current scene supports progression.

---

## Main Python File

### `disaster_response.py`

This file contains the complete game implementation.

It includes:

- Pygame initialization
- Window configuration
- Audio loading
- Image loading
- Font configuration
- Game states
- Story definitions
- Dialogue handling
- Text animation
- UI buttons
- Menu system
- Mode selection
- Level selection
- Gameplay logic
- Decision handling
- Success and failure outcomes
- Scene transitions
- Screen-shake effects
- Main game loop

---

## Requirements File

### `requirements.txt`

The current dependency list is:

```text
pygame
```

---

## Educational Purpose

The project demonstrates how an interactive application can be used to communicate disaster-response concepts through:

- Scenario-based learning
- Interactive decision making
- Visual storytelling
- Audio guidance
- Simulation
- Game-based learning

The project is intended as a software prototype and educational simulation.

---

## Development Approach

The project combines software-development concepts with interactive simulation.

The implementation includes:

```text
Python
   │
   ├── Pygame
   │
   ├── Game State Management
   │
   ├── Story Logic
   │
   ├── Event Handling
   │
   ├── Audio Integration
   │
   ├── Image Rendering
   │
   ├── Animation
   │
   └── User Interaction
```

---

## Future Enhancements

Possible future improvements include:

- Additional disaster scenarios
- Multiple playable levels
- Expanded Easy, Medium, and Hard modes
- More decision points
- Additional emergency situations
- Additional voice narration
- More interactive training scenarios
- Improved scoring and progress tracking
- More educational content
- Additional visual effects
- Improved accessibility features
- Scenario completion tracking
- More advanced gameplay logic

---

## Project Status

**Current Status:** Prototype / Academic Project

The current version implements the core interactive disaster-training experience with one primary scenario and a framework for adding additional levels and scenarios.

---

## Author

**Mohammed Thoufeeq Ali S M**

### GitHub

[MdThoufeeq](https://github.com/MdThoufeeq)

---

## Project Repository

[Disaster Response Training Game – Python Pygame](https://github.com/MdThoufeeq/Disaster-Response-Training-Python-Pygame)

---

## License

No specific open-source license has been added to this repository at this time.
