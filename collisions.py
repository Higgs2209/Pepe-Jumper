import pygame


class Collide():
    def __init__(self, pepe):
        pepe = self.pepe




    def platform_collide(self, platform_group, platform, jump_fx):
        if pygame.sprite.spritecollide(self.pepe, platform_group, False, pygame.sprite.collide_mask):
            # check if player is above rectangle
            # print(platform.rect.centery)
            if self.pepe.rect.bottom > platform.rect.centery:
                if self.pepe.vel_y > 0:
                    # I don't think I need the below line
                    # Make pepe bounce
                    self.pepe.dy = 0
                    self.pepe.vel_y = -20
                    jump_fx.play()
                # pepe.rect.bottom = platform.rect.top

    def enemy_collide(self, enemy_group):
        enemy_collision = False
        if pygame.sprite.spritecollide(self.pepe, enemy_group, False, pygame.sprite.collide_mask):
            # print('collide')
            enemy_collision = True
        return enemy_collision
