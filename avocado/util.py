import pygame

def render_text(text: str, line: int=0, font_size: int=16, **kwargs):
    "render text"
    #pos = [10, 8 + font_size*line]
    font = pygame.font.Font(kwargs.get('font_id', None), font_size)
    surf = font.render(text, True, (155,255,200))
    return surf
