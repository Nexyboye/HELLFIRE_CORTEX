import pygame
import numpy


# character position relative to the origo:
#   radius          between 0-infinity      0.d
#   time_angle      between t-x             1.d
#   polar_angle     between x-y             2.d
#   azimuthal_angle between y-z             3.d






pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Relativistic Engine")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()