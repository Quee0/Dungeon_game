import pygame
import numpy as np
from random import randint, choice
from level import Level, Chest, Floor_item
from sys import exit

pygame.init()

class Heart(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image = pygame.transform.scale(heart_img,(32,32))
		self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.moving = False
		self.back_while_moving = False
		self.hp = 0
		self.eq_show = False
		self.eq_size = 14
		self.heart_group = pygame.sprite.Group()
		self.items = []
		self.speed = 8

		self.add_hp(5)
		self.image = pygame.transform.scale(player_img,(64,64))
		self.rect = self.image.get_rect(topleft = (4*64,6*64))
	def resize_img(self,s): 
		self.image = pygame.transform.scale(player_img, (s,s))
	def move(self,key):
		if not self.moving and level.can_move(self.rect,key):
			# chest opening
			for chest in chests:
				if chest.can_open(
					(player_group.sprite.rect.center[0] - 64,player_group.sprite.rect.center[1]) if key == 'a'
					else (player_group.sprite.rect.center[0] + 64,player_group.sprite.rect.center[1]) if key == 'd'
					else (player_group.sprite.rect.center[0],player_group.sprite.rect.center[1]- 64) if key == 'w'
					else (player_group.sprite.rect.center[0],player_group.sprite.rect.center[1]+ 64)): 
					self.back_while_moving = True
					chest.start_opening()
					floor_items.add(Floor_item(chest.content_id,(chest.rect.x+17,chest.rect.y+6)))
			choice(step_sounds).play()
			for i in range(4): particle1.add_particle([self.rect.midbottom[0],self.rect.midbottom[1]],4,[randint(-1,1),randint(-1,1)],WHITE)
			self.counter = 0
			self.direction = key
			self.moving = True
	def execute_movement(self):
		if self.moving:
			self.counter += self.speed
			if self.counter<=32: self.resize_img(64+self.counter//2)
			else: self.resize_img((64-self.counter//2)+self.counter//2)
			if not self.back_while_moving or (self.counter<=32 and self.back_while_moving == True):
				if self.direction == 'a':self.rect.x -= self.speed
				elif self.direction == 'd':self.rect.x += self.speed
				if self.direction == 'w':self.rect.y -= self.speed
				elif self.direction == 's':self.rect.y += self.speed
			else:
				if self.direction == 'a':self.rect.x += self.speed
				elif self.direction == 'd':self.rect.x -= self.speed
				if self.direction == 'w':self.rect.y += self.speed
				elif self.direction == 's':self.rect.y -= self.speed
			if self.counter == 64:
				# get items from the floor
				for floor_item in floor_items:
					if self.rect.collidepoint(floor_item.rect.center) and len(self.items) < self.eq_size:
						self.items.append(floor_item.id)
						floor_item.kill()
				self.back_while_moving = False
				self.moving = False
				self.counter = 0
	def display_eq(self):
		WIN_HLR.blit(standard_font.render(f'{len(self.items)}/{self.eq_size}',False,WHITE),(20,60))
		if self.eq_show:
			eq_bg_border_handler = pygame.Surface((WIDTH//2,HEIGHT//2))
			eq_bg_border_handler.fill(WHITE)
			WIN_HLR.blit(eq_bg_border_handler,eq_bg_border_handler.get_rect(center=(WIDTH//2,HEIGHT//2)))
			eq_bg_handler = pygame.Surface((WIDTH//2-8,HEIGHT//2-8))
			WIN_HLR.blit(eq_bg_handler,eq_bg_handler.get_rect(center=(WIDTH//2,HEIGHT//2)))

			WIN_HLR.blit(eq_text,(eq_text.get_rect(center=(WIDTH//2,160))))
			row_counter = 0
			for num, item in enumerate(player_group.sprite.items):
				if row_counter >= 7: row_counter = 0
				row_counter += 1
				WIN_HLR.blit(item_imgs[item],(35*row_counter+280,180+(num//7)*35),special_flags=pygame.BLEND_RGBA_ADD)

	def add_hp(self,num): 
		self.hp += num
		for i in range(num):self.heart_group.add(Heart((40*len(self.heart_group)+ 16,16)))
	def remove_hp(self,num):
		self.hp -= num
		for i in range(num):
			for i in range(4): particle1.add_particle([self.heart_group.sprites()[-1].rect.center[0],self.heart_group.sprites()[-1].rect.center[1]],15,[randint(-1,1),randint(-1,1)],BLOOD_RED)
			self.heart_group.remove(self.heart_group.sprites()[-1])
	def update(self):
		self.execute_movement()
		self.display_eq() 

class Enemy(pygame.sprite.Sprite):
	def __init__(self, type_, pos):
		super().__init__()
		self.animation_index = 0
		self.animation_speed = 0.1
		if type_ == 'bat': 
			self.frames = [pygame.transform.scale(img,(64,64)) for img in bat_walk]
			self.image = self.frames[0]
		self.rect = self.image.get_rect(topleft = pos)
	def animation(self):
		self.animation_index += self.animation_speed
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]
	def update(self):
		self.animation()

class Particle:
	def __init__(self):
		self.particles = []
	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][0] += particle[2][0]
				particle[0][1] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(WIN_HLR,particle[3],particle[0],int(particle[1]))
	def add_particle(self,pos,radius,direction,color):
		self.particles.append([pos,radius,[direction[0],direction[1]],color])
	def delete_particles(self):
		particles_handler = [particle for particle in self.particles if particle[1] > 1]
		self.particles = particles_handler

WIDTH, HEIGHT = 900, 500
actual_width, actual_height = WIDTH, HEIGHT

DARKEST = (17,0,28)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLOOD_RED = (106,4,15)

FPS = 60
CLOCK = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN_HLR = WIN.copy()
player_img = pygame.image.load('textures/character.png').convert_alpha()
heart_img = pygame.image.load('textures/heart.png').convert_alpha()
item_imgs = [pygame.transform.scale(pygame.image.load(f'textures/item{id_}.png').convert_alpha(),(32,32)) for id_ in range(3)]
bat_walk = [pygame.image.load(f'textures/bat{i}.png').convert_alpha() for i in range(1,4)]
step_sounds = [pygame.mixer.Sound(f'audio/step{i}.wav') for i in range(1,6)]
bg_ambient = pygame.mixer.Sound('audio/bg_ambient_music.wav')
standard_font = pygame.font.Font('font/standard.TTF',22)
eq_text = standard_font.render('Equipment:',False,WHITE)

particle1 = Particle()
level = Level('fsdafsfd',WIN_HLR)
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())
enemies = pygame.sprite.Group()
chests = pygame.sprite.Group()
floor_items = pygame.sprite.Group()

enemies.add(Enemy("bat",(3*64,2*64)))
bg_ambient.play()

# player_group.sprite.items = [0,1,2,0,1,0,1,2,1,1,0,2,1]
chests.add(Chest((5*64,3*64),0))
chests.add(Chest((8*64,4*64),1))
chests.add(Chest((9*64,4*64),2))

while True:
	CLOCK.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a: player_group.sprite.move('a')
			elif event.key == pygame.K_d: player_group.sprite.move('d')
			if event.key == pygame.K_w: player_group.sprite.move('w')
			elif event.key == pygame.K_s: player_group.sprite.move('s')

			if event.key == pygame.K_e: player_group.sprite.eq_show = not player_group.sprite.eq_show
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	chests.update()
	enemies.update()
	player_group.update()
	WIN_HLR.fill(BLACK)
	level.run()

	# print(player_group.sprite.items)
	chests.draw(WIN_HLR)
	floor_items.draw(WIN_HLR)
	player_group.draw(WIN_HLR)
	enemies.draw(WIN_HLR)

	particle1.emit()
	player_group.sprite.heart_group.draw(WIN_HLR)
	player_group.sprite.display_eq()

	WIN.blit(pygame.transform.scale(WIN_HLR,[actual_width,actual_height]),(0,0))
	pygame.display.update()