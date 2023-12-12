Author: bogpok
import pygame as pg
from config import *
import math as m
from random import randint
from game_data import fy_simple1

def timeToString(time):
    secs = m.floor(time % 60)
    mins = int(time // 60)
    return str(mins)+":"+str(secs)

def show(screen, text, x, y, color = 'black', size = 32, alpha = 255):
    # Display ang
    font = pg.font.Font('./assets/Roboto-Bold.ttf', size)
    text = font.render(str(text), True, color)            
    textRect = text.get_rect()            
    textRect.left = x
    textRect.top = y
    text.set_alpha(alpha) 
    screen.blit(text, textRect)

def loadImg(image_src, scale = 1):
    image = pg.image.load(image_src).convert_alpha()

    # we can change image size
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    # now find the center of the image - offset
    dx = size[0]/2
    dy = size[1]/2

    return image, (dx, dy)

from csv import reader
def import_csv_layout(csv_path):
    csv_in_list = []
    # map represents csv_path
    with open(csv_path) as map1:
        level = reader(map1, delimiter = ',')
        for row in level:
            csv_in_list.append(list(row))
        return csv_in_list

def import_cut_graphic(image_src):
    image, center = loadImg(image_src)
    tilesetSize = TILESETSIZE
    tilesetList = []
    for row in range(tilesetSize[1]):
        for col in range(tilesetSize[0]):
            x = col*TILESIZE
            y = col*TILESIZE
            new_surf = pg.Surface((TILESIZE,TILESIZE))
            new_surf.blit(image, (0, 0), pg.Rect(x,y,TILESIZE,TILESIZE))
            tilesetList.append(new_surf)
    return tilesetList




def getDirection(position):
    x = position[0]
    y = position[1]
    r = (x**2 + y**2)**0.5
    if r == 0:
        return 0,0,0
    else:
        # ex, ey, radius
        return x/r, y/r, r

def filterByDeleteMarker(obj):            
            return not obj.deleteMarker


class Moon():
    def __init__(self, central):
        self.orbit = {
            'r': 70,
            'angSpeed': 0.1,
            'ang': 0
        }        
        self.R = 6
        self.rect = pg.Rect(central, (self.R, self.R))        
        self.rect.x = central[0]
        self.rect.y = central[1] - self.orbit['r']
        

    def update(self, screen, central):
        self.rect.x = central[0]
        self.rect.y = central[1]        
        self.orbit['ang'] += self.orbit['angSpeed']
        self.revolve(self.orbit['ang'])
        pg.draw.circle(screen, "white", (self.rect.x, self.rect.y), self.R)

    def revolve(self, ang):
        dx = m.sin(ang)*self.orbit['r']
        dy = (1-m.cos(ang))*self.orbit['r']
        self.rect.centerx += dx
        self.rect.centery += dy - self.orbit['r']

class RelativeDirection2d():
    def __init__(self, start, end):
        """
        Relative direction between two dots
        start, end:
            (x, y)
        """
        self.recalc(start, end)

    def recalc(self, start, end):
        self.start = start
        self.end = end

        self.x = self.start[0] - self.end[0]
        self.y = self.start[1] - self.end[1]
         
        self.ex, self.ey, self.r = getDirection((self.x, self.y))
        self.real_r = self.r
        self.ang = m.atan2(self.ey, self.ex)

    def restrictR(self, minR, maxR):
        if self.r > maxR:
            self.r = maxR                     
        elif self.r < minR:
            self.r = minR 
        self.x = self.ex * self.r
        self.y = self.ey * self.r

    def getTransformBack(self):
        # get back to global coordinates        
        x = self.start[0] - self.x
        y = self.start[1] - self.y
        return x, y



class extendsSprite(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rel_gt = RelativeDirection2d((0.,0.),(0.,0.))
        # Compensation angle
        self.compAng = 0

    def followDir(self, to_obj, center):
        """
        Follows to_obj object
        """
        self.rel_gt.recalc(
            (self.rect.centerx, self.rect.centery),
            (to_obj.rect.centerx, to_obj.rect.centery)
        )
        self.angdeg = 180 - (self.rel_gt.ang - self.compAng)/m.pi*180
            
        self.image = pg.transform.rotate(self.image_0, self.angdeg)
        self.center = center
        self.rect = self.image.get_rect(center = self.center)

    



class Player(extendsSprite):    
    def __init__(self, image_src, initial_pos, obstacleGroup, movetype = "manual"): 
        super().__init__()   
        self.image, self.offset = loadImg(image_src, 2)
        # initial position
        self.image_0 = self.image
        self.rect = self.image.get_rect(center=initial_pos)
        
        # Collision box
        c = (self.rect.w+self.rect.h)/(m.cos(m.pi/4)*2)        
        self.collBox = pg.Rect(self.rect.center, (c,c))
                
        self.speed = pg.math.Vector2(0, 0)
        self.dirs = pg.math.Vector2(0, 0)

        self.speedMag = 300;

        self.compAng = -m.pi/2

        # Tiles
        self.obstacleGroup = obstacleGroup

        self.setMoveType(movetype)
        


    def updateCollBox(self):       
        self.collBox.center = self.rect.center
        

    def showCollBox(self):
        pg.draw.rect(screen, "blue", self.collBox)
        
    def controls(self, dt):
        keys = pg.key.get_pressed()
            
        if keys[pg.K_w]:
            self.speed.y = -self.speedMag
        elif keys[pg.K_s]:
            self.speed.y = self.speedMag
        else:
            self.speed.y = 0

        if keys[pg.K_a]:
            self.speed.x = -self.speedMag
        elif keys[pg.K_d]:
            self.speed.x = self.speedMag
        else:
            self.speed.x = 0

    def followAim(self, aim):
        pass

    def setMoveType(self, movetype):
        if not movetype in ["manual", "auto"]:
            raise Exception("Movetype can be only manual or auto")
        self.movetype = movetype

    def move(self, dt):

        if self.movetype == "manual":
            self.controls(dt)

        elif self.movetype == "auto":
            # follow aim 
            pass

        if self.speed.x != 0 or self.speed.y != 0:            
            x = self.speed.x/self.speedMag*m.cos(m.pi/4) 
            y = self.speed.y/self.speedMag*m.cos(m.pi/4) 
            self.dirs.x = (1-y**2)**0.5       
            self.dirs.y = (1-x**2)**0.5 
            

        # Too fast diagonally
        if self.speed.x != 0 and self.speed.y != 0:            
            self.speed.x *= abs(self.dirs.x)
            self.speed.y *= abs(self.dirs.y)


        self.collBox.y += self.speed.y * dt        
        self.collBox.x += self.speed.x * dt   

        self.stayOnScreen()
        self.checkCollision2dBox()
        self.rect.center = self.collBox.center


    def update(self, dt):
        self.move(dt)        
        # self.showCollBox()

    def stayOnScreen(self):
        
        if self.collBox.right > screen.get_width():
            self.collBox.right = screen.get_width()            
        elif self.collBox.left < 0:
            self.collBox.left = 0            

        if self.collBox.bottom > screen.get_height():
            self.collBox.bottom = screen.get_height()            
        elif self.collBox.top < 0:
            self.collBox.top = 0
            
    def makeCollision2d(self, rect1, rect2):
        if rect2.colliderect(rect1): 
            dir2d = RelativeDirection2d(
                rect2.center, rect1.center
            )
            if abs(dir2d.x) > abs(dir2d.y):
                # axis = "horizontal"
                if dir2d.x > 0: # from left to right
                    rect1.right = rect2.left
                else:
                    rect1.left = rect2.right
                self.speed.y = 0 
        
            if abs(dir2d.x) < abs(dir2d.y):                    
                # axis = "vertical" 
                if dir2d.y > 0: # from top to bottom                    
                    rect1.bottom = rect2.top
                else:
                    rect1.top = rect2.bottom
                self.speed.x = 0

                 
    def checkCollision2dBox(self):
        """
        Checks:
        1. If there is a collision
        2. From which axis (horizontal/vertical)
        3. From which direction (left_right/top_bottom)
        """
        for obs in self.obstacleGroup:
            self.makeCollision2d(self.collBox, obs.rect)   

        # => Collision ideas
        # - "like aim like coll"
        #     - restrict by min ranius
        # - add tolerance - bad
        # - calc dir from RelativeDirection2d - good!          

                
    
          




class Aim():
    def __init__(self, player, atype = "mouse"):
        """
        atype = {"mouse","anotherplayer"}
        """
        self.player = player

        if not atype in ["mouse","anotherplayer"]:
            raise Exception('atype can only be "mouse" or "anotherplayer"')
        self.atype = atype

        self.image, self.offset = loadImg("./assets/aim.png", 1/12)
        self.image.set_colorkey("green")
        self.image.set_alpha(50) 

        self.maxR = 200 # maximum radius
        self.minR = 80
        self.rect = self.image.get_rect()
        self.r = 0
        self.ang = 0
        self.rel_pm = RelativeDirection2d(
            (self.player.rect.centerx, self.player.rect.centery),
            pg.mouse.get_pos()
        )

    def update(self, player, ):
        self.player = player

        if self.atype == "mouse":
            centerToFollow = pg.mouse.get_pos()
        elif self.atype == "anotherplayer":
            centerToFollow = self.bodyFollow.center

        # === AIM COORDS ===    
        self.rel_pm.recalc(
            (self.player.rect.centerx, self.player.rect.centery),
            centerToFollow
        )
        self.ang = self.rel_pm.ang
        self.rel_pm.restrictR(self.minR, self.maxR)
        
        self.x, self.y = self.rel_pm.getTransformBack()
        self.rect = self.image.get_rect(
            center = (
                self.x,
                self.y
            )
        )
        
        # === UPDATE PLAYER ===
        self.player.followDir(self, (self.player.rect.centerx, self.player.rect.centery))

    def forcePlayerToFollow(self):
        self.player.speed.x = -1*self.player.rel_gt.ex*self.player.speedMag/2
        self.player.speed.y = -1*self.player.rel_gt.ey*self.player.speedMag/2



    def draw(self, screen):
        # Show aim image
        screen.blit(self.image, self.rect)

        # Display ang
        text = "aim: {ang:.2f}".format(ang=self.ang)
        show(screen, text, self.rect.right, self.rect.bottom, 'green')
        
    def setBodyToFollow(self, bodyFollow):
        self.bodyFollow = bodyFollow

class Gun(extendsSprite):
    # inheritance from Sprite class to use its methods
    def __init__(self):
        # call parent class init
        super().__init__()
        self.image, self.offset = loadImg("./assets/pistol.png", 1/12)
        self.image_0 = self.image        
        self.rect = self.image.get_rect()

        self.rel_gt = RelativeDirection2d(
            (self.rect.centerx, self.rect.centery),
            (0,0)
        )
        self.angdeg = 0;
        
        self.blocked = False
        sound_vol = 0.1
        self.sounds = {"fire":pg.mixer.Sound("./assets/fire1.mp3")}
        for sound in self.sounds.values():
            sound.set_volume(sound_vol)

        self.gunDistance = 35

        self.magCap = 20 
        self.quantified = {
            "mag": self.magCap,
            "ammo": 50
        }
        self.damage = 25

    def update(self, dt, aim):     
        
        # position
        self.followDir(aim, (
                aim.player.rect.centerx,
                aim.player.rect.centery
            ))   

        self.revolve(self.rel_gt.ang, self.gunDistance)
        
    def extract(self, bullets):
        if self.quantified["mag"] > 0:
            self.quantified["mag"] -= 1;
            bullets.add(Bullet(self))
            self.sounds["fire"].play()
        # if self.quantified["mag"] == 0:
        #     self.block()
        
    def fire(self, bullets):
        if not self.blocked:
            self.extract(bullets)            
            self.block()

    def block(self):
        self.blocked = True     
    def unblock(self):
        self.blocked = False

    def revolve(self, ang, r):
        # dth to offset the gun
        dth = m.pi/2
        dx = m.sin(ang-dth*0.65)*r
        dy = (1-m.cos(ang-dth*0.65))*r
        self.rect.centerx += dx 
        self.rect.centery += dy - r
        

class Bullet(pg.sprite.Sprite):    
    def __init__(self, gun):
        super().__init__()
        self.image, self.offset = loadImg("./assets/bullet.png", 2)
        self.image_0 = self.image

        self.angdeg = gun.angdeg
        self.image = pg.transform.rotate(self.image_0, self.angdeg)
        self.rect = self.image.get_rect(center = gun.rect.center)
        self.gun = gun
        self.dirs = (self.gun.rel_gt.ex, self.gun.rel_gt.ey)

        self.time = 0
        self.speed = 800

        self.range = 400
        self.range_t = self.range/self.speed

    def update(self, dt):
        self.time += dt

        if self.time > self.range_t:
            self.kill()
            
        
        self.rect.x -= self.speed*self.dirs[0]*dt
        self.rect.y -= self.speed*self.dirs[1]*dt

    def draw(self, screen):
        # Show aim image
        screen.blit(self.image, self.rect)

class Person():
    """
    Wrapper for Player, Aim and Gun
    """        
    def __init__(self, image_src, initial_pos, tiles_group, aim_type = "mouse", movetype = "manual", show_aim = True):

        self.body = Player(image_src, initial_pos, tiles_group, movetype)        
        self.bodyWrapper = pg.sprite.Group(self.body)

        self.moon = Moon(self.body.rect.center)

        # Create aim object
        self.aim = Aim(self.body, aim_type)

        # Create gun object 
        self.gunDict = {"pistol":Gun()}
        self.guns = pg.sprite.RenderPlain([self.gunDict["pistol"],])
        self.currGun = "pistol"

        # Bullet list
        self.bullets = pg.sprite.Group()

        self.show_aim = show_aim

        self.quantified = {
            "health":100,
            "kevlar":0
        }

    def collides(self):

        # delete bullet on hitwall
        for hitwall in pg.sprite.groupcollide(self.bullets, self.body.obstacleGroup, 1, 0):
            pass

    def updateAddons(self, screen, dt):

        self.collides()

        self.moon.update(screen, self.body.rect.center)
        
        self.aim.update(self.body)
        if self.show_aim: self.aim.draw(screen)        

        for bullet in self.bullets:
            bullet.update(dt)
            bullet.draw(screen)


        self.guns.update(dt, self.aim)
        self.guns.draw(screen)

    def updatePrimary(self, screen, dt):

        self.bodyWrapper.update(dt)
        self.bodyWrapper.draw(screen)

    def update(self, screen, dt):
        self.updateAddons(screen, dt)
        self.updatePrimary(screen, dt)

    def events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gunDict[self.currGun].fire(self.bullets)                   
                
        elif event.type == pg.MOUSEBUTTONUP:
                self.gunDict[self.currGun].unblock()

    def takeDamage(self, damage):
        self.quantified["health"] -= damage

    def getCurrMag(self):
        return self.gunDict[self.currGun].quantified["mag"]
    def getCurrAmmo(self):
        return self.gunDict[self.currGun].quantified["ammo"]
    def getCurrDamage(self):
        return self.gunDict[self.currGun].damage
    def getCurrHP(self):
        return self.quantified["health"]
    def getCurrKevl(self):
        return self.quantified["kevlar"]


class Enemy(Person):   
    def __init__(self, image_src, init_pos, 
        tiles_group, aim_type = "anotherplayer", 
        movetype="auto"
    ):
        super().__init__(image_src,init_pos, tiles_group, aim_type, movetype)       
        self.R = 50
        # self.rect = pg.Rect(initial_pos, (self.R*2, self.R*2))
        self.deleteMarker = False   
        self.show_aim = False     
        
    def setBodyToFollow(self, bodyFollow):
        self.aim.setBodyToFollow(bodyFollow)
        self.body.makeCollision2d(self.body.collBox, bodyFollow.rect) 

    def firePeriodic(self, period = 30):        
        if m.floor(timestamp*100) % period == 0:
            self.gunDict[self.currGun].unblock()
            self.gunDict[self.currGun].fire(self.bullets) 

    def update(self, screen, dt):
        self.updateAddons(screen, dt)
        # => Aim update bodyToFollow
        self.aim.forcePlayerToFollow()
        self.updatePrimary(screen, dt)

        self.firePeriodic(200)
        self.showHP(screen)


    def takeDamage(self, damage):
        super().takeDamage(damage)
        if self.quantified["health"] <= 0:  
            global score          
            score += 1
            self.deleteMarker = True

    def showHP(self, screen):
        if self.body.collBox.collidepoint(pg.mouse.get_pos()):
            x, y = self.body.collBox.topleft
            x-=50
            show(screen, 'Enemy. Health: '+str(self.getCurrHP()), x, y, color='red', alpha=180, size=20)

    
    
    
class Tile(pg.sprite.Sprite):
    def __init__(self, initial_pos, size, tileImage = None):
        super().__init__()
        if tileImage:
            self.image = tileImage
        else:
            self.image = pg.Surface(size)
            color = (60,50,20)
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft = initial_pos)

    



def createEnemy(timestamp, enemyGroup, period = 25):
     
    if int(timestamp*100) % period == 0:
        x = randint(1, screen.get_width())
        y = randint(1, screen.get_width())
        enemyGroup.add(Enemy((x,y)))


def buildUI(screen, hp, kevl, timer, mag, ammo, score):
    """
    0 screen.get_width()
    0 screen.get_height()
    """
    color = (210, 180, 120)
    dy = 50
    ui_top = screen.get_height() - dy

    hp_x = 20
    dx = 120
    kevl_x = hp_x + dx

    alpha = 200

    # === Footer ===

    show(screen, '+  '+str(hp), hp_x, ui_top, color=color, alpha=alpha)
    show(screen, '¤  '+str(kevl), kevl_x, ui_top, color=color, alpha=alpha)
    
    show(screen,'Ҩ  '+str(timer), screen.get_width()/2-50, ui_top, color=color, alpha=alpha)
    _dy = 150
    show(screen,str(mag)+" | ", screen.get_width() - _dy-70, ui_top, color=color, alpha=alpha)
    show(screen,str(ammo)+' ◊', screen.get_width() - _dy, ui_top, color=color, alpha=alpha)

    # === other ===

    text = "Frags: {score}".format(score=score)
    show(screen, text, screen.get_width() - 200, dy, color=color, alpha=alpha)


    
    

    

class Map:
    def __init__(self, map_data, surface):
        self.display_surface = surface
        self.map_layout = import_csv_layout(map_data['walls'])
        # row(col) 
        self.tiles = pg.sprite.Group()
        self.tileSize = TILESIZE

        # self.tilesetImage = loadImg("./assets/Textures-64.png")

        self.tilesetList = import_cut_graphic("./assets/Textures-64.png")
        # Set length and height to screen size
        # self.length = self.display_surface.get_lenght()
        # self.height = self.display_surface.get_height()

        for row in range(len(self.map_layout)):
            for col in range(len(self.map_layout[row])):
                id = int(self.map_layout[row][col])
                if id > -1:
                    row = int(row)
                    col = int(col) 
                    
                    self.tiles.add(Tile(
                        (col*self.tileSize, row*self.tileSize), 
                        (self.tileSize, self.tileSize),
                        tileImage = self.tilesetList[id]
                    ))
                    

    def traceTilemapId(self):
        for row in range(len(self.map_layout)):
            for col in range(len(self.map_layout[row])):
                if int(self.map_layout[row][col]) > -1:
                    row = int(row)
                    col = int(col)                            
                    show(self.display_surface, self.map_layout[row][col], col*self.tileSize, row*self.tileSize)       
    def draw(self):
        self.tiles.draw(screen)
        # self.traceTilemapId()




def main():
    # pygame setup
    pg.init()
    pg.display.set_caption("Counter Strike PY")
    global screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    clock = pg.time.Clock()
    running = True
    dt = 0
    global timestamp
    timestamp = 0

    global score
    score = 0

    # Map
    level_map = Map(fy_simple1, screen)
    tiles = level_map.tiles

    
    

    # Manage persons - player and enemies    

    player = Person(
        "./assets/person_topdown.png",
        (0, screen.get_height() / 2),
        tiles
    )

      
    # Enemies
    enemies = []#pg.sprite.Group()

    enemies.append(Enemy(
        "./assets/terr_topdown2.png",
        (screen.get_width(), screen.get_height() / 2),
        tiles
    ))
    


    while running:
        # limits FPS to 60
        # It also will compute how many milliseconds have passed 
        # since the previous call   
             
        dt = clock.tick(FPS) / 1000
        timestamp += dt

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # poll for events
        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            player.events(event)

                   
    

        # === Show level ===
        level_map.draw()

        # === Persons update ===
        # for bullhit in pg.sprite.groupcollide(player.bullets, enemies, 1, 1):
        #     score+=1

        player.update(screen, dt)
        for enemy in enemies:
            enemy.setBodyToFollow(player.body)            
            enemy.update(screen, dt)

            for bullhit in pg.sprite.spritecollide(enemy.body, player.bullets, 1):
                # Player shoots at enemy
                enemy.takeDamage(player.getCurrDamage())
                
            for bullhit in pg.sprite.spritecollide(player.body, enemy.bullets, 1):
                # Enemy shoots player
                player.takeDamage(enemy.getCurrDamage())

        # filter enemies
        enemies = list(filter(filterByDeleteMarker, enemies))


        

        # === Build UI ===
        
        buildUI(screen, 
            hp = player.getCurrHP(), 
            kevl = player.getCurrKevl(), 
            timer = timeToString(timestamp), 
            mag = player.getCurrMag(), 
            ammo = player.getCurrAmmo(), 
            score = score,
        )


        # flip() the display to put your work on screen
        pg.display.flip()

        

    pg.quit()


if __name__ == "__main__":
    main()