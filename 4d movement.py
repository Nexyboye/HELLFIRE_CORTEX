import pygame
import numpy



# character position relative to the origo:
#   radius          between  -              0.d     0 - infinity
#   time_angle      between t-x             1.d     0 - 2pi
#   polar_angle     between x-y             2.d     0 - 2pi
#   azimuthal_angle between y-z             3.d     0 - 2pi

# speed will be constant 1


position = np.array([300,300])

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Relativistic Engine")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()