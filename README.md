# Ringette Game

A simple 2D Ringette game where players can pass and shoot the ring to score goals.

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```

## Building the Executable

To create a standalone executable:

1. Install the build requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```
   python build.py
   ```

3. The executable will be created in the `dist` directory.

## How to Play

- Use arrow keys to move your player
- Press SPACE to pass/shoot the ring
- Score goals by getting the ring into the opponent's net
- Avoid the opposing team's players

## Controls

- ↑ - Move up
- ↓ - Move down
- ← - Move left
- → - Move right
- SPACE - Pass/Shoot 

## Requests for More Features
- AI players? 
   - collisions
- Add AI on own team
- Add goalies
- Add passing over blue lines
   - Add free pass plays
- Add 5 second goal count
- Add crease violation
- Add advantage and free pass plays when blocking players
- Add pass instead of shot option
- Add point and click instead of space?
- Shooting on an angleV2
   - click and drag?
- Add 30 second shot clockV2
   - make it actually work
