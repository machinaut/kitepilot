#!/usr/bin/env python
# demo.py - draw a demo of the plane flying
import pygame, math

pygame.init()
# make sure we run at most at a specific FPS
fps = pygame.time.Clock()

surface = pygame.display.set_mode((1280,720))
# Path center and lemniscate width
center = (1280/2, 250)
width  = 500.0

sky = pygame.Color(50,242,255)
grn = pygame.Color(0,174,17)

t = 0.0
# loop until forever. goddamn robots.
while True:
    fps.tick(60) # go at most 30FPS
    # Path of travel is a Lemniscate
    x = (width * math.cos(t)) / (1 + math.sin(t)**2)
    y = (width * math.sin(t) * math.cos(t)) / (1 + math.sin(t)**2)
    pt = (center[0] + int(x), center[1] + int(y))
    t += .03
    surface.fill(sky)
    pygame.draw.circle(surface, grn, pt, 44, 0)
    pygame.display.update()
