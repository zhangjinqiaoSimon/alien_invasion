import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	'''一个对飞船发射的子弹进行管理的类'''
	def __init__(self,ai_settings,screen,ship):
		'''在飞船所处的位置创建一个子弹对象'''
		super().__init__()
		self.screen = screen
		
		self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)  #在（0,0）处创建一个表示子弹的矩形，在设置正确的位置
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		self.y = float(self.rect.y) #存储用小数表示子弹位置
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed
	
	'''向上移动子弹'''
	def update(self):
		'''更新y值'''
		self.y -= self.speed_factor
		self.rect.y = self.y
	
	'''在屏幕上绘制子弹'''
	def draw_bullet(self):
		pygame.draw.rect(self.screen,self.color,self.rect)
