import pygame

from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from coreboard import Scoreboard

def run_game():
	'''初始化游戏并创建一个屏幕对象'''
	pygame.init()  #初始化背景设置
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))   #设置屏幕大小
	pygame.display.set_caption('外星人入侵')   #设置窗口的名称
	
	stats = GameStats(ai_settings)
	
	'''创建一艘飞船'''
	ship = Ship(screen,ai_settings)
	
	'''创建分数'''
	sb = Scoreboard(ai_settings,screen,stats)
	
	play_button = Button(ai_settings,screen,'Play')
	
	bullets = Group()  #创建一个用于存储子弹的编组
	aliens = Group()   #创建一个用于存储外星人的编组
	
	gf.creat_fleet(ai_settings,screen,ship,aliens)
	 
	'''开始游戏的主循环'''
	while True:
		
		'''监视键盘和鼠标事件'''
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
		if stats.game_active:  #只在游戏处在活跃的状态中才调用的元素
			ship.update()  #控制飞船的左右移动
			bullets.update()  #Group中的每个子弹都调用update方法
			
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)  #子弹管理
			#print(len(bullets))
			gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)   #外星人移动
		
		'''每次循环都重绘屏幕'''
		'''让最近绘制的屏幕可见，就是不停的刷新'''
		gf.update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button)

run_game()
