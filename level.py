import pygame
from support import csv_to_tilemap, slice_to_tiles

class Floor_item(pygame.sprite.Sprite):
	def __init__(self,id_,pos):
		super().__init__()
		self.id = id_
		self.image = pygame.transform.scale(pygame.image.load(f'textures/item{id_}.png').convert_alpha(),(32,32))
		self.rect = self.image.get_rect(topleft=pos)

class Chest(pygame.sprite.Sprite):
	def __init__(self,pos,content_id):
		super().__init__()
		self.opening = False
		self.opened = False
		self.counter = 0
		self.content_id = content_id
		self.sound = pygame.mixer.Sound(f'audio/chest_sound.wav')
		self.frames = [pygame.transform.scale(pygame.image.load(f'textures/chest{i}.png').convert_alpha(),(64,64)) for i in range(1,3)]
		self.image = self.frames[0]
		self.rect = self.image.get_rect(topleft=pos)
	def start_opening(self):
		if not self.opening: 
			self.opening = True
			self.sound.play()
	def can_open(self,pos):
		if not self.opened and self.rect.collidepoint(pos[0],pos[1]): return True
		return False
	def update(self):
		if self.opening and not self.opened:
			if self.counter <= 10/2: self.rect.y -= int(10-self.counter)
			else: 
				self.image = self.frames[1]
				self.rect.y += int(self.counter)
			if self.counter == 10:
				self.counter = 0
				self.opened = True
			self.counter += 1

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect(topleft=pos)
class Level:
	def __init__(self,Level_data,surface):
		self.display_surf = surface

		self.wall_tiles = slice_to_tiles('textures/wall_tilemap.png')
		self.terrain = self.generate_tilemap(csv_to_tilemap('levels/level_0.csv'),'terrain')
	def generate_tilemap(self,layout,type_):
		tiles = pygame.sprite.Group()
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				if cell != '-1':
					if type_ == 'terrain':
						tiles.add(Tile((col_index*64,row_index*64),self.wall_tiles[int(cell)]))
		return tiles
	def can_move(self,player_pos,direction):
		x_move, y_move = 0,0
		if direction == 'a': x_move = -64
		elif direction == 'd': x_move = 64
		elif direction == 'w': y_move = -64
		elif direction == 's': y_move = 64

		for tile in self.terrain:
			if tile.rect.collidepoint((player_pos.center[0]+x_move,player_pos.center[1]+y_move)): return False
		return True
	def run(self):
		self.terrain.draw(self.display_surf)