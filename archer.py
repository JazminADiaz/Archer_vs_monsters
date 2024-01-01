import pygame

pygame.init()
scren_x=1700
screen_y=500
screen = pygame.display.set_mode((scren_x, screen_y))
pygame.display.set_caption('Archer')
clock = pygame.time.Clock()

left = False
right =False
jump= False
arrow_shoot= False
alive=True
enemy1_shoots=0
level=1
vel_sides=10
vel_mosters=1
gravity=1
height=20
y_vel=height
arrow_image = pygame.image.load(f'archer/img/arrow.png').convert_alpha()
arrow_image= pygame.transform.scale(arrow_image, (int(arrow_image.get_width() * 0.1), int(arrow_image.get_height() * 0.1)))
instructions_image=pygame.image.load(f'archer/img/instructions.png').convert_alpha()
#floor method, add as many images as necessary to fill the screen
def floor(path):
    floor=pygame.image.load(path).convert_alpha()
    y=screen_y-floor.get_height()/2
    box_floor=floor.get_rect()
    x=int((floor.get_width())/2) 
    floors_num=scren_x/floor.get_width()
    floors_num=int(floors_num)
    for i in range(0,floors_num+2):
        box_floor.center=(x*i*2,y)
        screen.blit(floor, box_floor)
#game method
def game(mosters_num):
    win=0
    winning=False
    game_over=False
    #display life 
    life_display(f'lifes: {100-heroine.heroine_wounds} ', font,10,35)
    floor(f'archer/img/grass.png')
    # heroine
    heroine.move(left,right,jump)
    heroine.show()
    #enemys
    for i in range (mosters_num):
        monster_list[i].move()
        monster_list[i].show()
        monster_list[i].kill()
        #chek if the heroine died or a monster reached the left side of the screen
        if monster_list[i].game_over==1 or heroine.alive==False:
            game_over=True
    #check if all the mosters are death
        if monster_list[i].alive==False:
            win+=1
    if win==mosters_num:
        winning=True

    #arrows
    arrows_group.update()
    arrows_group.draw(screen)

    #Game over
    return game_over, winning
    
#level menu method
def level_menu():
    mosters_num=0
    play=False

    screen.blit(instructions_image, (scren_x/2, 10))

    level1_pressed=level1_button.draw()
    if level1_pressed:
        mosters_num=1
    level2_pressed=level2_button.draw()
    if level2_pressed:
        mosters_num=3
    level3_pressed=level3_button.draw()
    if level3_pressed:
        mosters_num=5

    if mosters_num>0:
        play=True

    return  play,mosters_num
    
#first menu method
def first_menu():
    global game_running
    go_to_levels=False
    start_menu=start_button.draw()
    if start_menu:
        go_to_levels=True
    exit_game_b=exit_button.draw()
    if exit_game_b:
        game_running= False

    return go_to_levels

#mosters class
class mosters(pygame.sprite.Sprite):
    def __init__(self,x,y,num_monster):
        pygame.sprite.Sprite.__init__(self)
        monster =pygame.image.load(f'archer/img/moster{num_monster}.png').convert_alpha()
        monster= pygame.transform.scale(monster, (int(monster.get_width() * 0.2), int(monster.get_height() * 0.2)))

        self.image=monster
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.moster_wounds =0
        self.alive=True
        self.killing=False
        self.num_monster= int(num_monster)
        self.game_over=0
        
    def move (self):
    #check if they reach the left side
     #move the mosters to the left and change velocity according to monster
        if self.killing==False and self.rect.x>=0:
            if self.rect.x<=5 and self.alive==True:
                self.game_over=1
            self.rect.x-=vel_mosters*self.num_monster

    def show(self):
        #define how many arrows kill the mosters
        if self.moster_wounds >=5:
            self.alive=False
        #show the mosters
        if self.alive==True:
            screen.blit(self.image, self.rect)
        

    def kill(self):
        #check if the mosters are in the same position than the heroine, if so reduce lifes
        if self.rect.x - heroine.rect.x < 20 and self.rect.x - heroine.rect.x >-20 and self.rect.y - heroine.rect.y < 20 and self.rect.y - heroine.rect.y >-20 and heroine.alive and self.alive:
            self.killing=True
            heroine.heroine_wounds+=1
        else:
            self.killing=False

    
class characters(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        frame = pygame.image.load(f'archer/img/0.png').convert_alpha()
        self.doll_height=y
        self.image=frame
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.collition=False
        self.heroine_wounds=0
        self.alive=True
        self.flip=False
    #move to the left, or right
    #add gravity for jumping
    def move (self,left,right, jump):
        global gravity, height, y_vel
        if right:
            self.rect.x+=vel_sides
            self.flip=False

        if left:
            self.rect.x+=-vel_sides
            self.flip=True

        if jump==True and self.collition==False:
            jump=False
            self.rect.y-=y_vel
            y_vel-=gravity
            if (self.rect.y < -height):
                y_vel=height
        #stop falling if it's in the ground height
        if self.rect.y >345:
            self.rect.y=self.doll_height-45
            gravity=1
            height=20
            y_vel=height
            self.collition= True

    def show(self):
        #Define the wounds the heroine can have
        if self.heroine_wounds >=100:
            self.alive=False
        #show the heroine and flip to the right or left
        if self.alive==True:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            
       
#create the arrow, send it to the corresponding direction, and check for collition with mosters
class arrows(pygame.sprite.Sprite):
    def __init__(self,x,y, flip):
        pygame.sprite.Sprite.__init__(self)
        self.image=arrow_image
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.flip=flip
        

    def update(self):
        #move the arrow to the left or right (not beyond the screen width)
        if self.rect.x< scren_x:
            if self.flip==False:
                self.rect.x+=10
            else:
                self.rect.x-=10
        else:
            self.kill()
        #check if an arrow collide with the mosters
        for i in range(mosters_num):
            if monster_list[i].alive:
                if pygame.sprite.spritecollide(monster_list[i], arrows_group, False):
                    monster_list[i].moster_wounds+=1
                    self.kill()



#place a botton and check if the button was pressed
class Button():
    def __init__(self,x,y, button):
        pygame.sprite.Sprite.__init__(self)
        self.image=button
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.mouse_down=False
        
    def draw(self):
        mouse_pos=pygame.mouse.get_pos()
        action=False

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]==True and self.mouse_down==False:

                self.mouse_down=True
                action=True
            if pygame.mouse.get_pressed()[0]==0:
                self.mouse_down=False
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
        





#first menu buttons check
start =pygame.image.load(f'archer/img/START.png').convert_alpha()
exit =pygame.image.load(f'archer/img/EXIT.png').convert_alpha()
start_button=Button(scren_x/2, 100, start)
exit_button=Button(scren_x/2, 300, exit)

#second menu buttons check
level1=pygame.image.load(f'archer/img/LEVEL1.png').convert_alpha()
level2=pygame.image.load(f'archer/img/LEVEL2.png').convert_alpha()
level3=pygame.image.load(f'archer/img/LEVEL3.png').convert_alpha()
level1_button=Button(scren_x/3, 100, level1)
level2_button=Button(scren_x/3, 250, level2)
level3_button=Button(scren_x/3, 400, level3)
go_to_levels=False

#game check
mosters_num=0
play=False

#actual game settings

#life display
font = pygame.font.SysFont('arialblack', 30)

def life_display(text, font, x, y):
	img = font.render(text, True, (0,0,0))
	screen.blit(img, (x,y))
#heroine
heroine= characters(200, 345)
#ememys
monster_list = []

enemy1= mosters(scren_x, 350, '1')
enemy2= mosters(scren_x-100, 350, '2')
enemy3= mosters(scren_x-300, 350, '3')
enemy4= mosters(scren_x-500, 350, '4')
enemy5= mosters(scren_x-700, 350, '5')

monster_list = [enemy1,enemy2,enemy3,enemy4,enemy5]
#arrows
arrows_group = pygame.sprite.Group()
cont=0


#initialize game
game_running=True
game_over=False
winning=False



while game_running:

    clock.tick(60)
    screen.fill((255, 204, 153))
    #first menu
    if go_to_levels==False:
        go_to_levels=first_menu()
    #level menu
    if go_to_levels==True and play==False:
        play, mosters_num=level_menu()
        
    #actual game
    if play and game_over==False and winning==False:

        game_over, winning=game(mosters_num)

        #collide with the floor
        if heroine.collition==True:
            jump=False
            heroine.collition=False
        
        #shoot arrows one by one
        if arrow_shoot and cont==0:
            cont=20
            arrow = arrows(heroine.rect.centerx + (0.6 * heroine.rect.size[0]), heroine.rect.centery-15, heroine.flip)
            arrows_group.add(arrow)

        if cont>0 and cont<=40:
            cont-=1
    #final tittle
    if game_over==True:
        font1 = pygame.font.SysFont('arialblack', 150)
        life_display("GAME OVER", font1, 550, 150)
    if winning==True:
        font1 = pygame.font.SysFont('arialblack', 150)
        life_display("YOU WON", font1, 550, 150)


    #check for keydown

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left= True
            if event.key == pygame.K_d:
                right= True
            if event.key == pygame.K_w:
                jump= True
            if event.key == pygame.K_s:
                arrow_shoot= True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left= False
            if event.key == pygame.K_d:
                right= False
            if event.key == pygame.K_s:
                arrow_shoot= False
        if event.type== pygame.QUIT:
            game_running= False



    pygame.display.update()

pygame.quit()