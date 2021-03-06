import sys

import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

'''按键按下的事件'''
def keydown_event(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	
		'''空格增加一颗子弹'''
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	
		'''点击q退出游戏'''
	elif event.key == pygame.K_q:
		sys.exit()

'''按键拿起的事件'''
def keyup_event(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	for event in pygame.event.get():   #事件循环
		if event.type == pygame.QUIT:  #如果事件是退出事件，则退出系统
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			keydown_event(event,ai_settings,screen,ship,bullets)
		
		elif event.type == pygame.KEYUP:
			keyup_event(event,ship)
		
		#点击按钮开始
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y =  pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

'''对点击的坐标与按钮进行对比'''
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	button_chacked = play_button.rect.collidepoint(mouse_x,mouse_y)  #判断鼠标坐标是否是在矩形内,返回的值为true或者false
	if button_chacked and not stats.game_active:  #只有在按键范围内且游戏状态为false的时候点击才有效
		ai_settings.initilize_dynamic_settings()
		pygame.mouse.set_visible(False)  #设置鼠标不可见
		stats.reset_stats()  #重置游戏设置
		stats.game_active = True

		'''重新绘制图片'''
		sb.prep_score()
		sb.prep_hight_score()
		sb.prep_level()
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty() #清空外星人和子弹
		
		creat_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()  #创建外星人群和把飞船移动至中间

def update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button):
	'''每次循环都重绘屏幕'''
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()  #画船
	
	sb.show_score()  #显示分数
	
	aliens.draw(screen)  #画外星人
	
	#如果游戏处于非活跃状态，那么绘制按钮
	if not stats.game_active:
		play_button.draw_button()
	
	'''让最近绘制的屏幕可见，就是不停的刷新'''
	pygame.display.flip()

'''子弹的设置'''
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)   #飞出屏幕的子弹删除掉
	#检测子弹与外星人的碰撞
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

'''检测子弹与外星人碰撞以及消灭光外星人后的举动'''
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)  #groupcollide返回的是一个字典，若有碰撞则返回字典
	if collisions:  #判断字典是否存在
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	 
	if len(aliens) == 0:
		bullets.empty()  #清空所有子弹
		ai_settings.increase_speed()  #增加速度
		stats.level += 1
		sb.prep_level()
		creat_fleet(ai_settings,screen,ship,aliens)

'''发射子弹的代码'''
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def creat_fleet(ai_settings,screen,ship,aliens):
	'''创建外星人群'''
	alien = Alien(ai_settings,screen)
	alien_num = get_alien_num_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	
	for row_number in range(number_rows):
		for alien_number in range(alien_num):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien =Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
		
def get_alien_num_x(ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	'''计算屏幕可以容纳几行外星人'''
	avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(avaliable_space_y / (2 * alien_height))
	return number_rows
	
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
	check_fleet_deges(ai_settings,aliens)
	aliens.update()
	
	if pygame.sprite.spritecollideany(ship,aliens):  #检测船与外星人是否碰撞
		ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
	
	check_alien_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
	if stats.ships_left > 0:
		stats.ships_left -= 1   #将ships_left减一
		
		'''清空子弹和外星人'''
		aliens.empty()
		bullets.empty()

		sb.prep_ships()
		
		creat_fleet(ai_settings,screen,ship,aliens)  #创建一群外星人
		ship.center_ship()  #把船放到中间
		
		sleep(0.5)  #暂停0.5秒
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)  #在当游戏结束时，鼠标光标可见

def check_fleet_deges(ai_settings,aliens):
	'''当外星人到达边缘是采取措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_flee_direction(ai_settings,aliens)
			break

def change_flee_direction(ai_settings,aliens):
	'''使整群外星人下移并改变方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.alien_down
	ai_settings.fleet_direction *= -1
	
def check_alien_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	'''检查是否有外星人到屏幕最底部'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:  #当外星人的底部碰到屏幕的底部
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			sb.prep_ships()
			break

def check_high_score(stats,sb):  #比较最高分与现在分数的大小
	if stats.score > stats.hight_score:
		stats.hight_score = stats.score
		sb.prep_hight_score()
