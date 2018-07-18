import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	def __init__(self,ai_settings,screen,stats):
		#初始化显示得分涉及的属性
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#设置显示得分的字体和颜色
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)
		
		#准备初始得分图像
		self.prep_score()
		self.prep_hight_score()
		self.prep_level()
		self.prep_ships()
	
	def prep_score(self):
		round_score = int(round(self.stats.score,-1))  #精确到10位
		score_str = '{:,}'.format(round_score)  #获得分数的内容，其中这是固定用法，用逗号分隔数字
		self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)  #分数编程图像
		#设置分数的位置
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
	
	def prep_hight_score(self):
		hight_score = int(round(self.stats.hight_score,-1))
		hight_score_str = '{:,}'.format(hight_score)
		self.hight_score_image = self.font.render(hight_score_str,True,self.text_color,self.ai_settings.bg_color)
		
		self.high_score_rect = self.hight_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = 20
	
	def show_score(self):   #显示分数
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.hight_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)

	def prep_level(self):
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color,self.ai_settings.bg_color)
		'''将等级放在分数下方'''
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right - 20
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		self.ships = Group()
		for ship_num in range(self.stats.ships_left):
			ship = Ship(self.screen, self.ai_settings)
			ship.rect.x = 10 + ship_num * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
