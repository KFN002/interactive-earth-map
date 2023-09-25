import os
import pygame
import requests


def get_pic(coord1, coord2, zoom, type_66):
    map_params = {
        "ll": ",".join([str(coord1), str(coord2)]),
        "z": str(zoom),
        "l": type_66,
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def show_pic(map_file, coord1, coord2, zoom):
    running = True
    curr = 0
    sc_size = width, height = 1200, 600
    surface = pygame.display.set_mode(sc_size)
    while running:
        if zoom < 5:
            k_move = 30
        else:
            k_move = 5 / (10 ** (zoom // 4))
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_PAGEUP] and zoom < 20:
            zoom += 1
        if key_pressed[pygame.K_PAGEDOWN] and zoom > 0:
            zoom -= 1
        if key_pressed[pygame.K_UP]:
            coord2 += k_move
        if key_pressed[pygame.K_DOWN]:
            coord2 -= k_move
        if key_pressed[pygame.K_LEFT]:
            coord1 -= k_move
        if key_pressed[pygame.K_RIGHT]:
            coord1 += k_move
        if key_pressed[pygame.K_TAB]:  # смена режима карты (aka "переключатель")
            curr = (curr + 1) % 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ch_types = ['map', 'sat', 'sat,skl']
        if coord1 > 180:
            coord1 = 180
        elif coord1 < - 180:
            coord1 = -180
        if coord2 > 85:
            coord2 = 85
        elif coord2 < -85:
            coord2 = -85
        map_file = get_pic(coord1, coord2, zoom, ch_types[curr])
        surface.blit(pygame.image.load(map_file), (500, 100))
        pygame.display.flip()
    os.remove(map_file)
    pygame.quit()


if __name__ == '__main__':
    print('Please write the coords:')
    coord1 = float(input())
    coord2 = float(input())
    toponym_to_find = 'Москва'
    zoom = 1
    pygame.init()
    show_pic(get_pic(coord1, coord2, zoom, 'map'), coord1, coord2, zoom)