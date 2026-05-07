import pygame as py
import PySimpleGUI as psg
import time  

# constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 750
BG_COLOR = (196,238,255)
B_COLOR = (3,180,255)

# non-constants
running = True

class button : 

    def __init__(self, screen, width, height, x, y, content, fontSize):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x 
        self.y = y
        self.content = content
        self.fontSize = fontSize
        
    def draw(self) : 

        width = self.width
        height = self.height
        x = self.x
        y = self.y 
        screen = self.screen
        content = self.content
        fontSize = self.fontSize
        
        font = py.font.SysFont("Arial", fontSize)
        text = font.render(content, True, (0,0,0))

        self.button = py.rect.Rect(x,y,width,height)
        
        py.draw.rect(screen, B_COLOR, self.button) 
        screen.blit(text,(x+self.width/2-text.get_rect().width/2,y+self.height/2-text.get_rect().height/2)) 
    
    
class textField: 
    
    def __init__(self, content,screen):
        self.content = content
        self.screen = screen 
        self.x = 50
        self.y = 50
        self.wrapLength = 250
        self.fontSize = 30

        self.font = py.font.SysFont("Arial", self.fontSize)

        self.text = self.font.render(self.content, True, (0,0,0), wraplength=self.wrapLength)

    def add_d_button(self,y) :
        self.d_button = button(screen,50,25,SCREEN_WIDTH-100,y,"Done",15)
        self.d_button.draw()

class scroll_able:
     
    def __init__(self, screen):
        self.screen = screen
        self.bg_width = SCREEN_WIDTH - 100
        self.bg_height = SCREEN_HEIGHT - 50
        
        self.si_width = 10
        self.si_height = 40

    def set(self,y):

        self.background = py.rect.Rect(50,25,self.bg_width,self.bg_height)
        self.scroll_indicator = py.rect.Rect(SCREEN_WIDTH-self.si_width,y,self.si_width,self.si_height)

        self.draw()

    def draw(self):
        screen = self.screen

        py.draw.rect(screen, (255,255,255), self.background)
        py.draw.rect(screen, (146,146,146), self.scroll_indicator)


def popup_input():
    msg = psg.popup_get_text("Task: ")
    return str(msg)

def displayTasks(y):

    for i in range(0,len(tasks)) : 

        if i != 0 :
            y += tasks[i-1].text.get_height()+5 

        # print("y: ", y)
        
        tasks[i].add_d_button(y)
        text_rect = tasks[i].text.get_rect(topleft=(tasks[i].x,y))
        py.draw.rect(screen, B_COLOR, text_rect)
        screen.blit(tasks[i].text,(tasks[i].x,y))
        
py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
s_color = (196,238,255)
screen.fill(BG_COLOR)

b_addTask = button(screen, 100, 50, SCREEN_WIDTH-150, SCREEN_HEIGHT-100,"+",30)
b_addTask.draw()
t_textField = textField("Add a new task!", screen)
s_scroll = scroll_able(screen); 

task_y = 25

tasks = []

py.display.flip()

while running : 
    # time.sleep(0.1)

    for event in py.event.get() :
        if event.type == py.QUIT : 
            running = False; 
        
        if event.type == py.MOUSEWHEEL: 
            print(event.y)
            if event.y < 0: 
                # print('down')
                task_y -= 50
            
            if event.y > 0:
                # print('up')
                task_y += 50

            if task_y < 25 :
                task_y = 25
            
            continue

        if event.type == py.MOUSEBUTTONUP : 
            if b_addTask.button.collidepoint(event.pos) : 

                print("pressed")
                tasks.append(textField(popup_input(), screen))
                print(tasks)
            else :
                for d_tasks in tasks: 
                    if d_tasks.d_button.button.collidepoint(event.pos) :
                        tasks.remove(d_tasks)

        
        

    screen.fill(s_color)
    s_scroll.set(task_y)
    displayTasks(task_y)
    
    b_addTask.draw()

    py.display.update()
                                
