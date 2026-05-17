import pygame as py
import PySimpleGUI as psg
import time  

from datetime import datetime
from datetime import date
import pandas as pd

# constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 750
BG_COLOR = (196,238,255)
BUTTON_COLOR = (3,180,255)

# non-constants
running = True

# ALL classes used 
class button : 

    def __init__(self, width, height, x, y, content, fontSize):
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
        content = self.content
        fontSize = self.fontSize
        
        font = py.font.SysFont("Arial", fontSize)
        text = font.render(content, True, (0,0,0))

        self.button = py.rect.Rect(x,y,width,height)
        
        py.draw.rect(screen, BUTTON_COLOR, self.button) 
        screen.blit(text,(x+self.width/2-text.get_rect().width/2,y+self.height/2-text.get_rect().height/2)) 

class textField: 
    
    def __init__(self, content, start_m):
        self.content = content
        self.x = 50
        self.y = 50
        self.wrapLength = 250
        self.fontSize = 30

        self.font1 = py.font.SysFont("Arial", self.fontSize)
        self.text = self.font1.render(self.content, True, (0,0,0), wraplength=self.wrapLength)
        
        self.start_m = start_m 
        print("start_m exists: ", start_m)
            

    def set(self) :
        x = self.x
        y = self.y
        text = self.text

        text_rect = text.get_rect(topleft=(x,y))

        py.draw.rect(screen, BUTTON_COLOR, text_rect)
        screen.blit(text,(x,y))

    def add_d_button(self,y) :
        self.y = y

        self.d_button = button(50,25,SCREEN_WIDTH-100,y,"Done",15)
        self.d_button.draw()

class scroll_able:
     
    def __init__(self):
        self.bg_width = SCREEN_WIDTH - 100
        self.bg_height = SCREEN_HEIGHT - 50
        
        self.si_width = 10
        self.si_height = 100

    def set(self,y):

        self.background = py.rect.Rect(50,25,self.bg_width,self.bg_height)
        self.scroll_indicator = py.rect.Rect(SCREEN_WIDTH-50-self.si_width,y,self.si_width,self.si_height)

        self.draw()

    def draw(self):

        py.draw.rect(screen, (255,255,255), self.background)
        py.draw.rect(screen, (146,146,146), self.scroll_indicator)

class progress_bar :

    def __init__(self):
        self.container_width = 35
        self.container_height = 400
        self.container_x = SCREEN_WIDTH-self.container_width
        self.container_y = 50

        self.inner_width = 25
        self.inner_height = 1 # this means it's full: self.container_height-10 
        self.inner_x = self.container_x+(self.container_width-self.inner_width)/2
        self.inner_y = self.container_y + 5
    
    def set(self): 
        self.container_rect = py.rect.Rect(self.container_x, self.container_y, self.container_width, self.container_height)
        self.inner_rect = py.rect.Rect(self.inner_x, self.inner_y, self.inner_width, self.inner_height)

    def draw(self):

        py.draw.rect(screen, (0,0,0),self.container_rect)
        py.draw.rect(screen, (0,255,0),self.inner_rect)

class productivityBar :

    def __init__(self):
        self.container_width = 35
        self.container_height = 200
        self.container_x = SCREEN_WIDTH-self.container_width
        self.container_y = 500

        self.inner_width = 25
        self.inner_height = 1 # this means it's full: self.container_height-10 
        self.inner_x = self.container_x+(self.container_width-self.inner_width)/2
        self.inner_y = self.container_y+5
    
    def set(self): 
        self.container_rect = py.rect.Rect(self.container_x, self.container_y, self.container_width, self.container_height)
        self.inner_rect = py.rect.Rect(self.inner_x, self.inner_y, self.inner_width, self.inner_height)

    def draw(self):

        py.draw.rect(screen, (0,0,0),self.container_rect)
        py.draw.rect(screen, (0,0,255),self.inner_rect)

# functions used 
def popup_input():
    msg = psg.popup_get_text("Task: ")
    return str(msg)

def moveTasks(y):

    for i in range(0,len(tasks)) : 

        if i != 0 :
            y += tasks[i-1].text.get_height()+5 


        tasks[i].y = y
        # tasks[i][1] = y

        # print("y: ", y)
        
        tasks[i].add_d_button(y)
        tasks[i].set()

def bar_percentage() :
    if total_tasks == None or total_tasks == 0: 
        return

    p_bar.inner_height = (p_bar.container_height-10)*(total_tasks-len(tasks))/total_tasks
    p_bar.set()
    # print("percentage: ",(p_bar.container_height-10)*(total_tasks-len(tasks))/total_tasks)

def update_productive(current_task) : 
    timeNow = (datetime.now().hour)+(datetime.now().minute)/60
    tasks_completed = total_tasks - len(tasks)
    duration = (timeNow-current_task.start_m)

    if duration == None or duration == 0 :
        return

    prod_bar.inner_height = (tasks_completed/(duration))*0.01*prod_bar.container_height

    print("tasks completed: ", tasks_completed)
    print("Time in minutes NOW: ", timeNow)
    print("Time in minutes when CREATED: ", current_task.start_m)
    print("productivity bar hiehgt: ", prod_bar.inner_height)
    prod_bar.set()
    prod_bar.draw()

def save() : 

    timesMade = []

        # convert all of the tasks button into it's content
    for i,items in enumerate(tasks) : 
        tasks[i] = items.content
        timesMade.append(items.start_m)

    df = pd.DataFrame(tasks,columns=['Tasks']) 
    df['Time'] = date.today().day # save the current day ONLY if it is different from what it was when it started
    df['TaskLength'] = total_tasks
    df['TimeTaskCreated'] = timesMade
    df.to_csv('saveFile')

def load_file(tasks) :

    currentTime = tasks.at[0,'Time']
    taskLen = tasks.at[0,'TaskLength']
    converted_tasks = []

    print("task length: ",taskLen)

    for i in range(0,len(tasks['Tasks'])):
        print(tasks.at[i,'Tasks'], " : ")
        converted_tasks.append(textField(str(tasks.at[i,'Tasks']),tasks.at[i,'TimeTaskCreated']))

    return converted_tasks,currentTime,taskLen

# MAIN game/visuals set up and game loop
py.init()

try: 
    tasks = pd.read_csv('saveFile')
    tasks,currentTime,total_tasks = load_file(tasks)
except: 
    print("file empty/non existant")
    tasks = []
    currentTime = date.today()
    total_tasks = 0
    taskTime = None

start = time.perf_counter()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BG_COLOR)

b_addTask = button(100, 50, SCREEN_WIDTH-150, SCREEN_HEIGHT-100,"+",30)
s_scroll = scroll_able(); 
p_bar = progress_bar()
prod_bar = productivityBar()

p_bar.set()
bar_percentage()
prod_bar.set()
prod_bar.draw()
# print('tasks: ', tasks)
update_productive(tasks[len(tasks)-1])

task_height = 0
running = True
task_y = 25

end = time.perf_counter()
print("Elapsed time: ", end-start, " seconds")

py.display.flip()

while running : 

    # start = time.perf_counter()

    screen.fill(BG_COLOR)
    s_scroll.set(-task_y)
    b_addTask.draw()
    moveTasks(task_y)
    p_bar.draw()
    prod_bar.draw()

    py.display.update()
    # time.sleep(0.1)

    for event in py.event.get() :
        if event.type == py.QUIT : 
            save()
            running = False; 
            break
        
        if event.type == py.MOUSEWHEEL: 
            # print(event.y)
            if event.y < 0: 
                # print('down')
                task_y -= 50
            
            if event.y > 0:
                # print('up')
                task_y += 50

            # print(task_y)
            if task_y > -25:
                task_y = 25

            continue

        if event.type == py.MOUSEBUTTONUP : 
            if b_addTask.button.collidepoint(event.pos) : 

                print("pressed")
                taskTime = datetime.now().hour+datetime.now().minute/60
                tasks.append(textField(popup_input(),taskTime))

                total_tasks += 1
                bar_percentage()
                print(tasks)
            else :
                for d_tasks in tasks: 
                    if d_tasks.d_button.button.collidepoint(event.pos) :
                        
                        tasks.remove(d_tasks)
                        bar_percentage()
                        update_productive(d_tasks)

                        if len(tasks) == 0 : 
                            total_tasks = 0 

                        print(total_tasks)
                        print(len(tasks))

    # end = time.perf_counter()
    # print("Elapsed time: ", end-start, " seconds")
                        
                                
