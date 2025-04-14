import pygame
from pygame.locals import *
import struct
from .util import render_text

ENTITY_POS_FRMT = '!hhff'

class BasePlayer(pygame.sprite.Sprite):
    "Base player class, with logic and no graphics"
    username: bytes=b'Herobrine'
    rect: pygame.rect.FRect
    mv: pygame.math.Vector2
    ip: str # IP address of this player
    def __init__(self, username: str='Harry', pos: tuple[int,int] = (100,100)):
        super().__init__()
        self.username = username.encode('utf-8')
        self.rect = pygame.FRect(pos, (50,50))
        self.mv = pygame.Vector2(0)
    def update_location(self, packet: bytes):
        left, top, mvx, mvy = struct.unpack(ENTITY_POS_FRMT, packet)
        self.rect.left = left
        self.rect.top  = top
        self.mv.x = mvx
        self.mv.y = mvy
    def export_location(self) -> bytes:
        left = int(self.rect.left)
        top  = int(self.rect.top)
        mvx = self.mv.x
        mvy = self.mv.y
        return struct.pack(ENTITY_POS_FRMT, left, top, mvx, mvy)
    def update_pos(self, dt: float=1000/60):
        mv = self.mv * (dt / 1000)
        self.rect.move_ip(mv)

class RenderedPlayer(BasePlayer):
    surf: pygame.surface.Surface
    def __init__(self, username: str='Harry', pos: tuple[int,int] = (100,100)):
        super().__init__(username, pos)
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill([200,200,200])
    def update_keypresses(self, keys):
        speed = 150 # pixels per second
        mv = pygame.Vector2(0)
        if keys[K_w]:
            mv.y -= speed
        if keys[K_s]:
            mv.y += speed
        if keys[K_a]:
            mv.x -= speed
        if keys[K_d]:
            mv.x += speed
        self.mv = mv
    def render_nametag(self, surf: pygame.Surface):
        s = render_text(self.username.decode('utf-8'))
        r = s.get_rect(bottom=self.rect.top, centerx=self.rect.centerx)
        surf.blit(s,r)
