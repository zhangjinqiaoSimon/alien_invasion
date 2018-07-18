'''跟踪游戏的统计信息'''
class GameStats():
	def __init__(self,ai_settings):
		'''初始化统计信息'''
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False  #游戏处于活跃状态
		self.hight_score = 0  #设置最高分数
	
	def reset_stats(self):   #初始化游戏运行期间可能变化的统计信息
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
