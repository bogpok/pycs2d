# pycs2d
python version of CS2D - a two-dimensional conversion of the popular game Counter-Strike by Valve®.

<img src="/demo.gif" height="400">


# Stages

## Backbone

### Objectives

- Drawing circles
- Types of control

### Tasks

- Player and aim are represented as two circles
- You can move Player by wasd
- You can move aim by mouse


## Aim v2

### Objectives

- Drawing images, rescaling
- Adding functions
- Coordinates and directions

### Tasks

- Aim is a picture, not a circle
- Aim is restricted by some radius


## Aim v3

### Objectives

- Creating classes
- Class Methods and Properties

### Tasks

- Refactoring code to have aim as object


## First gun

### Objectives

- Refactor loadAim to loadImage
- Creating classes with inheritance
- Orientation

### Tasks

- Gun is presented on a screen as an image
- It is rotated as aim rotates


## Shooting

### Objectives

- Events
- Bullet object
- Object lists
- Sound

### Tasks

- There is a bullet on a mouse click
- The direction of a bullet is the same as aim (on the moment of click)
- The bullet has some **range** (it is not infinite)
- Bullet is deleted (as object) after:
	- Having pass specified range


## Player holds the gun

### Objectives

- Refactor Player
- Rotating Player
- Get new directions

### Tasks

- Define Player as Sprite
- Player should turn where aim is
- Gun should turn around the player with same direction
- Offset the gun position 


## Adding targets

### Objectives

- Collision
- Random positions of Enemies

### Tasks

- Some targets presented on a screen as circles
- Bullet is deleted (as object) after:
	- Having pass specified range
	- Hitting a target
- The target is deleted when bullet hits it


## Walls and Obstacles

### Objectives

- Player can not pass screen
- Tiles
- Collision with tiles

### Tasks

- Two Obstacles presented on a screen
- Bullet is deleted (as object) after:
	- Having pass specified range
	- Hitting a target
	- Hitting a wall


## Enemies attack

### Objectives

- Enemy collision
- Follow between objects

### Tasks

- Enemies will try to follow the player, aim and shoot at him
- Player can not go through enemies
- Enemies has same collision rules as a player:
	- can not go through walls
	- can not go through player


## UI

### Objectives

- Health points
- Damage
- Magazine counter

### Tasks

- Positions:
	HP | Kevlar | curr_mag | ammo | 
- When enemies bullet hit a player it lowers its HP

## fy map

### Objectives

- Tile design
- Tiled app
- Loading tiles in a game

### Tasks

- Create a small map called fight yard
0. Create CSV in tiled
1. import CSV file
2. import image (tileset)
3. use the data


## Game Over (GO) screen

### Objectives


- GO Screen UI
- GO Screen condition
- Restart button



## Weapons type mechanics

### Objectives

- Aim radius is different
- Shooting speed is different
- Spread is different
- Range is different

### Tasks

- Implement:
	- Pistol
	- Shotgun
	- Rifle
- Weapon is changed on keys: 1, 2, 3
- UI of changing the weapon


## Reload mechanics

### Objectives

- Reloading time
- Reloading bar
- Magazine size is different per weapon type


### Tasks

- Reloading weapons



## Collectibles v1 - ammunition 

### Objectives

- Collecting items
- Calculating magazine 
- Random appereance
- Can not fire when Magazine is empty


## Enemies range of view

### Objectives

- Range of view object

### Tasks

- Enemy will not attack Player if the Player is not in the range of view



## Viewport

### Objectives

- Make map larger then screen window

### Tasks

- Map is larger then screen window and it adapts as player moves (viewport)


## Extra

- Granades
- Kevlar
- Knife



# Objects to implement

This is a design exercise.
For each object specify its attributes and methods.

## Player

## Enemy

## Bullet

## Aim

