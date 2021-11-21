from csv import reader
import pygame
def csv_to_tilemap(path):
	with open(path) as map:
		tiles_csv = reader(map,delimiter=',')
		level = [row for row in tiles_csv]
		return(level)
def slice_to_tiles(path):
	surface = pygame.transform.scale(pygame.image.load(path).convert_alpha(),(256,320))
	tile_num_x = int(surface.get_size()[0] / 64)
	tile_num_y = int(surface.get_size()[1] / 64)
	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			surface_handler = pygame.Surface((64,64))
			surface_handler.blit(surface, (0,0),pygame.Rect(col*64,row*64,64,64))
			cut_tiles.append(surface_handler)

	return cut_tiles