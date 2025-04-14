import pygame
import socket
import avocado
import time
import sys

pygame.init()

HOST = ('0.0.0.0', avocado.PORT)

scr_w = 400
scr_h = 400
#username = ('user' + str(hash('hello world')))[:8]
username = sys.argv[-1][:8]

def update_status(*args):
    print(*args, ' '*24, end='\r', flush=True)
    #time.sleep(0.1)

update_status("Loading")

scr = pygame.display.set_mode([scr_w, scr_h])

players = pygame.sprite.Group()
player_usernames = [username.encode('utf-8')]
me = avocado.entity.RenderedPlayer(username)
players.add(me)

TICK = pygame.event.custom_type()
pygame.time.set_timer(TICK, 200)

run = 1
clk = pygame.time.Clock()
username = username.encode('utf-8')

update_status("Joining")

with avocado.network.new_sock() as sock:
    sock.connect(HOST)
    sock.send(b'JON')
    sock.send(username)

while run:
    dt = clk.tick(60)
    for event in pygame.event.get():
        if event.type == TICK:
            try:
                update_status("LSPing")
                with avocado.network.new_sock() as sock:
                    sock.connect(HOST)
                    sock.send(b'LSP')
                    sock.send(username) # important part of protocol
                    d = username
                    while d != b'.'*8:
                        #update_status("LSPing:", d)
                        if d not in player_usernames:
                            players.add(avocado.entity.RenderedPlayer(d.decode('utf-8')))
                            player_usernames.append(d)
                        d = sock.recv(8)
                update_status("Beaming state to server")
                with avocado.network.new_sock() as sock:
                    sock.connect(HOST)
                    sock.send(b'SET')
                    sock.send(username)
                    sock.send(me.export_location())
                update_status("Fetching state from server")
                for player in players:
                    if player is me: continue # optmisation and so on
                    with avocado.network.new_sock() as sock:
                        sock.connect(HOST)
                        sock.send(b'GET')
                        sock.send(player.username)
                        player.update_location(sock.recv(avocado.network.ENTITY_POS_FRMT_LEN))
            except BrokenPipeError:
                print("\033[1mBROKEN PIPE\033[0m, skipping tick...", file=sys.stderr)
        elif event.type == pygame.QUIT:
            update_status("Quitting")
            run = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = 0
    update_status("Rendering")
    scr.fill((0,0,0))
    me.update_keypresses(pygame.key.get_pressed())
    for player in players:
        player.update_pos(dt)
        scr.blit(player.surf, player.rect)
    pygame.display.flip()

pygame.quit()