#设置类，所有的设置都在这儿
class Settings():
	def __init__(self):
		'''初始化游戏的设置'''
		#屏幕的设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		#飞船速度设置
		self.ship_limit = 3 #飞船的数量
		
		'''子弹参数设置'''
		self.bullet_width = 3   #子弹宽度设置
		self.bullet_height = 15 #子弹长度设置
		self.bullet_color = 60,60,60  #子弹颜色的设置
		self.bullet_allowed = 3  #限制子弹的数量
		
		self.alien_down = 10 #外星人下降的速度
		
		self.speedup_scale = 1.1  #以什么样的速度加快游戏节奏
		self.initilize_dynamic_settings()
	
	def initilize_dynamic_settings(self):  #初始化随游戏进行而变化的设置
		self.ship_speed = 1.5
		self.bullet_speed = 1
		self.alien_speed_factor = 1
		
		self.fleet_direction = 1  #为1表示向右，-1表示向左
	
	def increase_speed(self):  #提高速度设置
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
