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

- Add passing over blue lines
  - Add free pass plays
- Add 5 second goal count
- Add crease violation
- Add advantage and free pass plays when blocking players
- Add pass instead of shot option
- Add point and right click instead of space?
- Shooting on an angleV2
  - click and drag?
- fix ring position when stabbing and give random chance not to pick it up.
- fix the stupid toolbar/ribbon

### Future Additions

#### Goalie

- Goalie sprites
- Goalie movement
- Goalie rings
- Taking control
- two different jerseys

#### Shot Clock

- reset on change of possesion
- reset on shot of specific goalie
- reset on penalties
- goalie rings on 0s or free passes

#### AI

- add players on your own team
  - collisions?
- pass to other players
- other players can pass and shoot
- call for the ring back
- add opposing team
- take control of different players

#### Score

- #|# instead of Score: #
