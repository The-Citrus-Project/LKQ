"""
Lemon Kingdom Quest: The Sorceror Arises
- Developed by: The Citrus Project
- Story: Nakamura Daiki, Yukimura Nobuko
- Main Programmer: Ethan Fyre of NaetherTechkd
- Citrish and Pholeth: Karl Schneider, Nikita Chekhov
- Sprite Design: Nikita Chekhov, Kobayashi Koji
- Concept Art: N/A
- Game Testing: Gregor Mikhailova
- Music: Frank Lawson, Kobayashi Koji
- NPC Text: Almyra Nayelie, Daniel Hunter
- Special Thanks: James Jamison
"""
# CHANGES FROM PREVIOUS VERSION:
"""
- 
- BUG FIXES
"""
# TO DO:
"""
- Make NPC Text wrap
- Add stat screen to pause menu
- FINISH CASTLE OF SECLUSION 
"""
from LKQ_Library import *

HERO_MOVE_SPEED = 200  # pixels per second
MAP_FILENAME = 'grasslands.tmx'               


# MAIN GAME CODE
def main():
    
    # INITIALIZATION
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = init_screen(WIN_WIDTH, WIN_HEIGHT)
    pygame.display.set_caption('Lemon Kingdom Quest: The Sorceror Arises')
    
    # SETUP
    
    # Player Creation
    movingsprites = pygame.sprite.Group()
    player = Hero(180, 180, "P1", 150, 150, 150, 150, 150, 0, 100000, 30)
    bob = Hero(180, 180, "P2", 150, 150, 150, 150, 140, 0, 100000, 30)
    bob2 = Hero(180, 180, "P3", 150, 150, 150, 150, 136, 0, 100000, 30)
    movingsprites.add(player)
    movingsprites.add(bob)
    movingsprites.add(bob2)
    players = [player, bob, bob2]
    for man in players:
        man.weapon = Glaive()
        man.armour = Ruby_vest(1, 0)
        man.update() 

    # Room Setup
    battles = [BattleTest(players, screen)]
    pauses = [PauseTest(player, screen)]
    rooms = []
    room_names = []
    rooms.append(grass_test(player, screen))
    rooms.append(grass_test2(player, screen))
    rooms.append(COSthroneroom(player, screen))
    rooms.append(COSchestTR(player, screen))
    rooms.append(COSchestLR(player, screen))
    rooms.append(COSchestTL(player, screen))
    rooms.append(COSchestLL(player, screen))
    rooms.append(COSfoyer(player, screen))
    rooms.append(COSstairR(player, screen))
    rooms.append(COSstairL(player, screen))
    rooms.append(COSTstair(player, screen))
    rooms.append(COSThallway(player, screen))
    rooms.append(COSTscribe(player, screen))
    rooms.append(COSTlounge(player, screen))
    rooms.append(COSTarmoury(player, screen))
    rooms.append(COSBstair0(player, screen))
    rooms.append(COSBdining(player, screen))
    rooms.append(COSBstair1(player, screen))
    rooms.append(COSBkitchen(player, screen))
    rooms.append(COSBservant(player, screen))
    rooms.append(COSBbattle(player, screen))
    rooms.append(COSBlocked0(player, screen))
    rooms.append(COSBhealth(player, screen))
    rooms.append(COSBchest(player, screen))
    rooms.append(COSBjailer(player, screen))
    rooms.append(COSBspiderhole(player, screen))
    rooms.append(COSBjail0(player, screen))
    rooms.append(COSBjail1(player, screen))
    rooms.append(COSBguard(player, screen))
    rooms.append(COSBstorage(player, screen))
  
    current_room_no = 22
    current_room = rooms[current_room_no]
    last_room_no = 1    
    room_names.append("grass_test")
    room_names.append("grass_test2")
    room_names.append("COSthroneroom")
    room_names.append("COSchestTR")
    room_names.append("COSchestLR")
    room_names.append("COSchestTL")
    room_names.append("COSchestLL")
    room_names.append("COSfoyer")
    room_names.append("COSstairR")
    room_names.append("COSstairL")
    room_names.append("COSTstair")
    room_names.append("COSThallway")
    room_names.append("COSTscribe")
    room_names.append("COSTlounge")
    room_names.append("COSTarmoury")
    room_names.append("COSBstair0")
    room_names.append("COSBdining")
    room_names.append("COSBstair1")
    room_names.append("COSBkitchen")
    room_names.append("COSBservant")
    room_names.append("COSBbattle")
    room_names.append("COSBlocked0")
    room_names.append("COSBhealth")
    room_names.append("COSBchest")
    room_names.append("COSBjailer")
    room_names.append("COSBspiderhole")
    room_names.append("COSBjail0")
    room_names.append("COSBjail1")
    room_names.append("COSBguard")
    room_names.append("COSBstorage")
    
    # VARIABLES

    # Text variables
    text_speed = 5
    test_text = "Kill all on sight. text box at 400 y-pixels!"
    text_displayed = False
    text_display = ""
    HeroName = "bob"

    # Sound Variables
    music_volume = 1
    SFX_volume = 1
    sword_swing = pygame.mixer.Sound("data/sounds/sword.ogg")
    sword_swing.set_volume(SFX_volume)
    save_file = "data/save files/save_1.txt"
    fade_time = 200 
    pygame.mixer.music.load(current_room.music)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    
    # Battle Variables
    deadplayers = [0, 0, 0]
    deadenemies = [0, 0, 0]
    display1, display2, display3, display4 = "", "", "", ""
    text1, text2, text3, text4 = "", "", "", ""

    # Pause Variables
    pauseoption = 0

    # Misc.
    time = 0
    speed = 6
    move_speed = speed  # * current_room.map_layer.zoom
    current_save = 1
    game_speed = 30
    game_mode = 1        # 0 - Start Screens, 1 - Overworld, 2 - Battle, 3 - Pause Menus
    clock = pygame.time.Clock()
    running = True

    while running:        
        # dt = clock.tick()/1000
        poll = pygame.event.poll
        event = poll()
        
        # EVENT HANDLING
        while event:
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYDOWN:
                if game_mode == 1:    
                    # Battle debugging
                    if event.key == pygame.K_b:
                        game_mode = 2
                        player.rect.x = 500
                        player.rect.y = 300
                        bob.rect.x = 570
                        bob.rect.y = 320
                        bob2.rect.x = 640
                        bob2.rect.y = 270
                        break
                    if event.key == pygame.K_p:
                        game_mode = 3
                        player.rect.x = -100
                        player.rect.y = -100
                        pygame.mixer.music.fadeout(fade_time)
                        pygame.mixer.music.load(pauses[0].music)
                        pygame.mixer.music.set_volume(music_volume)
                        pygame.mixer.music.play(-1)
                        break
                    # Text debugging
                    if event.key == pygame.K_5:
                        text_displayed = True
                    if event.key == pygame.K_6:
                        text_displayed = False
                    if event.key == pygame.K_7:
                        test_text = "Happy is the man who dies"
                        text_display = ""
                    # Change game speed
                    if event.key == pygame.K_0:
                        game_speed += 5
                    if event.key == pygame.K_9:
                        game_speed += -5
                    # Change text speed
                    if text_displayed:
                        if event.key == pygame.K_k:
                            text_speed = 1
                    # If Player is beside NPC display text box
                    if event.key == pygame.K_j:
                        if not text_displayed:
                            if len(current_room.npcs) > 0:
                                for npc in current_room.npcs:
                                    if not text_displayed:
                                        if npc.left or npc.right or npc.above or npc.below:
                                            test_text = npc.text
                                            text_display = ""
                                            text_displayed = True
                        elif text_displayed:
                            text_displayed = False
                        if len(current_room.chest_list) > 0:
                            for chest in current_room.chest_list:
                                if chest.contact:
                                    chest.take_items(player)
                    # if len(current_room.npcs) > 0:
                    #     for npc in current_room.npcs:
                    #         if event.key == pygame.K_j:
                    #             if not text_displayed:
                    #                 if npc.left or npc.right or npc.above or npc.below is True:
                    #                     test_text = npc.text
                    #                     text_display = ""
                    #                     text_displayed = True
                    #             elif text_displayed:
                    #                 text_displayed = False
                    elif event.key == K_EQUALS:
                        current_room.map_layer.zoom += .25

                    elif event.key == K_MINUS:
                        value = current_room.map_layer.zoom - .25
                        if value > 0:
                            current_room.map_layer.zoom = value

                    # TEMPORARY SAVING METHOD, REMOVE IN THE FUTURE
                    if event.key == K_v:
                        if current_save == 1:
                            save_file = "data/save files/save_1.txt"
                        elif current_save == 2:
                            save_file = "data/save files/save_2.txt"
                        elif current_save == 3:
                            save_file = "data/save files/save_3.txt"
                        f = open(save_file, "w")
                        f.write(str(player.rect.x) + "\n")
                        f.write(str(player.rect.y) + "\n")
                        f.write(str(current_room_no) + "\n")
                        f.write(HeroName + "\n")
                        f.write(str(player.money) + "\n")
                        f.close()
                        f = open("data/save files/temp_save.txt","w")
                        f.write(str(player.rect.x) + "\n")
                        f.write(str(player.rect.y) + "\n")
                        f.write(str(current_room_no) + "\n")
                        f.write(HeroName + "\n")
                        f.write(str(player.money) + "\n")
                        f.close()
                            
                    # TEMPORARY LOADING METHOD, REMOVE IN THE FUTURE
                    if event.key == K_c:
                        if current_save == 1:
                            save_file = "data/save files/save_1.txt"
                        elif current_save == 2:
                            save_file = "data/save files/save_2.txt"
                        elif current_save == 3:
                            save_file = "data/save files/save_3.txt"
                        f = open(save_file, "r")
                        player.rect.x = int(f.readline())
                        player.rect.y = int(f.readline())
                        current_room_no = int(f.readline())
                        HeroName = f.readline()[0:-1]
                        player.money = int(f.readline())
                        f.close()
                        player.old_x = player.rect.x
                        player.old_y = player.rect.y
                        current_room = rooms[current_room_no]
                        screen.fill(BLACK)
                        pygame.display.flip()
                        pygame.mixer.music.fadeout(fade_time)
                        pygame.mixer.music.load(current_room.music)
                        pygame.mixer.music.set_volume(music_volume)
                        pygame.mixer.music.play(-1)
                        
                    # if text is displayed stop all motion
                    if text_displayed:
                        player.change_x = 0
                        player.change_y = 0

                    # if text is not displayed control player motion
                    if not text_displayed:
                        # player movements
                        if event.key == K_UP or event.key == K_w:
                            player.changespeed(0, -move_speed)
                        elif event.key == K_DOWN or event.key == K_s:
                            player.changespeed(0, move_speed)
                        elif event.key == K_LEFT or event.key == K_a:
                            player.changespeed(-move_speed, 0)
                        elif event.key == K_RIGHT or event.key == K_d:
                            player.changespeed(move_speed, 0)
                if game_mode == 2:
                    if event.key == K_o:
                        player.stats['hp'] -= 10
                    if event.key == K_p:
                        player.stats['hp'] += 10
                        
                    if event.key == K_UP or event.key == K_w:
                        player.changespeed(0, -move_speed)
                    elif event.key == K_DOWN or event.key == K_s:
                        player.changespeed(0, move_speed)
                    elif event.key == K_LEFT or event.key == K_a:
                        player.changespeed(-move_speed, 0)
                    elif event.key == K_RIGHT or event.key == K_d:
                        player.changespeed(move_speed, 0)
                    if event.key == pygame.K_b:
                        game_mode = 1
                        player.battle_trigger = None
                        break
                if game_mode == 3:
                    if event.key == pygame.K_p:
                        game_mode = 1
                        player.rect.x = player.old_x
                        player.rect.y = player.old_y
                        pygame.mixer.music.fadeout(fade_time)
                        pygame.mixer.music.load(current_room.music)
                        pygame.mixer.music.set_volume(music_volume)
                        pygame.mixer.music.play(-1)
                        break
                    if event.key == K_DOWN or event.key == K_s:
                        pauseoption += 1
                        pauseoption %= 3
                    elif event.key == K_UP or event.key == K_w:
                        pauseoption -= 1
                        pauseoption %= 3
                    if event.key == K_j:
                        if pauseoption == 0:
                            if current_save == 1:
                                save_file = "data/save files/save_1.txt"
                            elif current_save == 2:
                                save_file = "data/save files/save_2.txt"
                            elif current_save == 3:
                                save_file = "data/save files/save_3.txt"
                            f = open(save_file, "w")
                            f.write(str(player.old_x) + "\n")
                            f.write(str(player.old_y) + "\n")
                            f.write(str(current_room_no) + "\n")
                            f.write(HeroName + "\n")
                            f.write(str(player.money) + "\n")
                            f.close()
                            f = open("data/save files/temp_save.txt", "w")
                            f.write(str(player.old_x) + "\n")
                            f.write(str(player.old_y) + "\n")
                            f.write(str(current_room_no) + "\n")
                            f.write(HeroName + "\n")
                            f.write(str(player.money) + "\n")
                            f.close()
                            print("Game has been saved!")
                        elif pauseoption == 1:
                            game_mode = 1
                            player.rect.x = player.old_x
                            player.rect.y = player.old_y
                            pygame.mixer.music.fadeout(fade_time)
                            pygame.mixer.music.load(current_room.music)
                            pygame.mixer.music.set_volume(music_volume)
                            pygame.mixer.music.play(-1)
                            break
                        elif pauseoption == 2:
                            running = False
                            break
                if event.key == K_ESCAPE:
                    running = False
                    break                
            elif event.type == KEYUP:
                if game_mode == 1:
                    # Change text speed
                    if text_displayed:
                        if event.key == pygame.K_k:
                            text_speed = 7
                    elif not text_displayed:
                            
                        if event.key == K_UP or event.key == K_w :
                            player.change_y = 0
                        elif event.key == K_DOWN or event.key == K_s:
                            player.change_y = 0
                        elif event.key == K_LEFT or event.key == K_a:
                            player.change_x = 0
                        elif event.key == K_RIGHT or event.key == K_d:
                            player.change_x = 0
                if game_mode == 2:
                    if event.key == K_UP or event.key == K_w :
                        player.change_y = 0
                    elif event.key == K_DOWN or event.key == K_s:
                        player.change_y = 0
                    elif event.key == K_LEFT or event.key == K_a:
                        player.change_x = 0
                    elif event.key == K_RIGHT or event.key == K_d:
                        player.change_x = 0
            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                    init_screen(event.w, event.h)
                    current_room.map_layer.set_size((event.w, event.h))                    
            event = poll()
        # GAME LOGIC
        if game_mode == 1:
            current_room.update(10*current_room.map_layer.zoom,time,text_displayed)
            player.move(current_room.wall_list, current_room.enemy_sprites, current_room.npcs, current_room.chest_list, current_room, (player.rect.width/2), time)
            
            if player.battle_trigger is not None:
                game_mode = 2
                player.rect.x = 500
                player.rect.y = 300
                bob.rect.x = 570
                bob.rect.y = 320
                bob2.rect.x = 640
                bob2.rect.y = 270
                pygame.mixer.music.fadeout(fade_time)
                pygame.mixer.music.load(battles[0].music)
                pygame.mixer.music.set_volume(music_volume)
                pygame.mixer.music.play(-1)
    
            # Handle room changes
            if player.rect.collidelist(current_room.moves) > -1:
                last_room_no = current_room_no
                current_room_no = room_names.index((current_room.moves_names[player.rect.collidelist(current_room.moves)]))
                current_room = rooms[current_room_no]
                (player.rect.x, player.rect.y, player.direction) = current_room.new_room(room_names[last_room_no])
                player.old_x = player.rect.x
                player.old_y = player.rect.y
                player.change_x = 0
                player.change_y = 0
                screen.fill(BLACK)
                pygame.display.flip()
                if rooms[last_room_no].music != current_room.music:
                    pygame.mixer.music.fadeout(fade_time)
                    pygame.mixer.music.load(current_room.music)
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(-1)

            # DRAWING CODE
            current_room = rooms[current_room_no]
            current_room.draw(screen)
            display_money(screen, str(player.money))
            # Text Boxes
            if text_displayed:
                display_text(screen, WIN_WIDTH, WIN_HEIGHT, text_display)
                if time % text_speed == 0:
                    text_display += test_text[:2]
                    test_text = test_text[2:]
            
            # debugging code
            texx("X: ", 5, 100, screen, RED, 20)
            texx(str(player.rect.x), 40, 100, screen, RED, 20)
            texx("Y: ", 5, 120, screen, RED, 20)
            texx(str(player.rect.y), 40, 120, screen, RED, 20)
            texx("FPS: ", 5, 150, screen, RED, 20)
            texx(str(round(clock.get_fps(), 0)), 60, 150, screen, RED, 20)

            # keep track of time
        if game_mode == 2:
            battles[0].draw(screen)
            battles[0].update()
            player.moveb(battles[0].wall_list, player.rect.width/2, time)
            bob.moveb(battles[0].wall_list, bob.rect.width / 2, time)
            bob2.moveb(battles[0].wall_list, bob2.rect.width / 2, time)
            # bob.rect.x, bob.rect.y = player.rect.x + 70, player.rect.y
            # bob2.rect.x, bob2.rect.y = player.rect.x + 140, player.rect.y
            for enemy in player.battle_trigger.group:
                battles[0].enemy_sprites.add(enemy)
                enemy.moveb(battles[0].wall_list, enemy.rect.width/2, time)
            players = battles[0].players
            enemies = player.battle_trigger.group
            battle_text(screen, display1, display2, display3, display4)
            battle_tick = .4
            fast_player = players[0]
            for enemy in enemies:
                enemy.tick = battle_tick * enemy.stats['speed']/fast_player.stats['speed']
                # print (enemy.name, enemy.stats['hp'], enemy.level)
                for hero in players:
                    if hero.type == enemy.bias:
                        enemy.aggro[players.index(hero)] = 10000
            for hero in players:
                hero.tick = battle_tick * hero.stats['speed']/fast_player.stats['speed']
                # print (hero.name, hero.stats['hp'], hero.level)
            for enemy in enemies:
                for hero in players:
                    if hero.status == 'dead':
                        enemy.aggro[players.index(hero)] = 0
                if enemy.status == 'dead':
                    enemy.gauge = 0
                    enemy.stats['hp'] = 0
                    enemy.aggro = [0, 0, 0]
                    deadenemies[enemies.index(enemy)] = 1
                else:
                    if enemy.gauge >= 100:
                        target = players[enemy.aggro.index(max(enemy.aggro))]
                        move = enemy.AI(target)
                        enemy.rect.centery -= 40
                        enemy.feet.midbottom = enemy.rect.midbottom
                        damage = damaged(enemy, target, move)
                        target.stats['hp'] -= damage
                        text1, text2, text3, text4, display1, display2, display3, display4 = text_queue(text1, text2, text3, text4, display1, display2, display3, display4, ("%s dealt %i damage to %s using %s." %(enemy.name, damage,  target.name,  move[0]) ))
                        enemy.gauge = 0
                        if target.stats['hp'] <= 0:
                            enemy.aggro[players.index(target)] = 0
                            text1, text2, text3, text4, display1, display2, display3, display4 = text_queue(text1, text2, text3, text4, display1, display2, display3, display4, ("%s fainted!" %(target.name)))
                            target.status = 'dead'
                            text_display = ""
                    enemy.gauge += enemy.tick

            for hero in players:
                if hero.status == 'dead':
                    hero.stats['hp'] = 0
                    hero.gauge = 0
                    deadplayers[players.index(hero)] = 1
                else:
                    if hero.gauge >= 100:
                        targ = randint(0, len(enemies) - 1)
                        while enemies[targ].status == 'dead':
                            targ = randint(0, len(enemies) - 1)
                        target = enemies[targ]
                        hero.rect.centery -= 40
                        hero.feet.midbottom = hero.rect.midbottom
                        move = hero.moves[0]
                        damage = damaged(hero, target, move)
                        target.stats['hp']  -= damage
                        text1, text2, text3, text4, display1, display2, display3, display4 = text_queue(text1, text2, text3, text4, display1, display2, display3, display4, ("%s dealt %i damage to %s using %s." %(hero.name, damage,  target.name,  move[0])))
                        target.aggro[players.index(hero)] += damage
                        hero.gauge = 0
                        if target.stats['hp'] <= 0:
                            text1, text2, text3, text4, display1, display2, display3, display4 = text_queue(text1, text2, text3, text4, display1, display2, display3, display4, ("%s fainted!" %(target.name)))
                            target.status = 'dead'

                    hero.gauge += hero.tick               
            if time % 4 == 0:
                display1 += text1[:1]
                text1 = text1[1:]
                display2 += text2[:1]
                text2 = text2[1:]
                display3 += text3[:1]
                text3 = text3[1:]
                display4 += text4[:1]
                text4 = text4[1:]
            if all(deadenemies):
                game_mode = 1
                player.battle_trigger = None
                pygame.mixer.music.fadeout(fade_time)
                pygame.mixer.music.load(current_room.music)
                pygame.mixer.music.set_volume(music_volume)
                pygame.mixer.music.play(-1)
            if all(deadplayers):
                game_mode = 1
                player.battle_trigger = None
                deadplayers = [0, 0, 0]
                deadenemies = [0, 0, 0]
                for hero in players:
                    hero.stats['hp'] = hero.stats['hp_max']
                    hero.status = 'alive'
                for enemy in enemies:
                    enemy.stats['hp'] = enemy.stats['hp_max']
                    enemy.status = 'alive'
                save_file = "data/save files/temp_save.txt"
                f = open(save_file, "r")
                player.rect.x = int(f.readline())
                player.rect.y = int(f.readline())
                current_room_no = int(f.readline())
                HeroName = f.readline()[0:-1]
                player.money = int(f.readline())
                f.close()
                player.old_x = player.rect.x
                player.old_y = player.rect.y
                current_room = rooms[current_room_no]
                screen.fill(BLACK)
                pygame.display.flip()
                pygame.mixer.music.fadeout(fade_time)
                pygame.mixer.music.load(current_room.music)
                pygame.mixer.music.set_volume(music_volume)
                pygame.mixer.music.play(-1)
        if game_mode == 3:
            pauses[0].draw(screen, pauseoption)
        time += 1
        clock.tick(game_speed)
        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        raise
