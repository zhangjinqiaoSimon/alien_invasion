import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self,screen,ai_settings):
		'''初始化飞船并设置其初始位置'''
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		'''加载飞船图像并获取其外接矩形'''
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		'''将每艘新飞船放在屏幕底部中央'''
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		self.center = float(self.rect.centerx)  #存储小数值
		
		self.moving_right = False  #移动标志
		self.moving_left = False   #移动标志
	
	def blitme(self):
		'''在指定位置绘制飞船'''
		self.screen.blit(self.image,self.rect)
	
	'''根据移动标志来移动飞船'''
	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:  #设定右边界
			self.center += self.ai_settings.ship_speed
		
		if self.moving_left and self.rect.left > self.screen_rect.left:   #设定左边界
			self.center -= self.ai_settings.ship_speed
		
		self.rect.centerx =self.center
	
	def center_ship(self):
		self.center = self.screen_rect.centerx
