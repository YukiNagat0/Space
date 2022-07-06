import sys 

from pygame import *
init()
from player import Player
from balls import Ball

scale = 3.0
spacing = 10
size = width, height = 320 * scale, 240 * scale
speed = [10, 10]
player_speed = 8
black = 0, 0, 0

# Initilize everything.
init()
screen = display.set_mode(size)
display.set_caption("Dodgeball")


class Item():    
    def __init__(self, type):
        self.type = type
        self.cargo = [Ball("bouncing")]


player = Player("left")
#player_sprites = sprite.RenderPlain((player,))
player_sprites = sprite.RenderPlain((player,))
ball_sprites = sprite.RenderPlain(())

#ball = image.load("ball.gif")
#ball_rect = ball.get_rect()
#ball_rect.move(50, 50)

# Fill background
background = Surface(screen.get_size())
background = background.convert()
background.fill((black))

screen.blit(background, (0,0))

actions = {
        K_DOWN: player.movedown,
        K_LEFT: player.moveleft,
        K_RIGHT: player.moveright,
        K_UP: player.moveup,
        }

while 1:
    for evnt in event.get():
        if evnt.type == QUIT: 
            sys.exit()
    
        if evnt.type == KEYDOWN:
            keys = key.get_pressed()
           
            if evnt.key == K_SPACE: 
                ball_sprites.add(player.throw())
                
            elif evnt.key in actions.keys():                
                actions[evnt.key]()
           
            elif evnt.key in [K_ESCAPE]:
                sys.exit(0)
            else:
                print("Uknown key. %s" % evnt.key)

            player.pickup(Item("ball"))

        elif evnt.type == KEYUP:
            if evnt.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                player.movepos = [0,0]
                player.state = "still"


    screen.blit(background, (0,0))

    ball_sprites.update()
    player_sprites.update()
    screen.blit(background, player.rect, player.rect)
    
    collided = []
    for ball in ball_sprites.sprites():

        #ball_sprites.remove(ball)
        #for c in sprite.spritecollide(ball, balls, True,
        #        sprite.collide_circle):
        #    collided.append(c)
        #ball_sprites.add(ball)
        print player.rect, ball.rect

        if ball.cleared_player() and ball.collided(player.rect):
            print "cleared player, and collided"
            ball.kill()
        else:
            print "still touching"

        if ball.is_dead():
            ball.kill()
        # Check ball against others for a collision
        if ball.thrown:
            ball.bounce(size, spacing)
        screen.blit(background, ball.rect, ball.rect)

#   for ball in sprite.spritecollide(player, ball_sprites, False,
#           sprite.collide_circle):
#       if ball.cleared_player():
#           print ball.cleared_player() #s.kill()

    for c in collided:
        print c
        ball_sprites.remove(c)


    #for b in sprite.spritecollide(player, ball_sprites, False,
    #        sprite.collide_circle):
    #    b.kill()

    ball_sprites.draw(screen)
    player_sprites.draw(screen)

    display.flip()
