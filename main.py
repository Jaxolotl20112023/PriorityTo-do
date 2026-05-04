import pygame as py
import PySimpleGUI as psg

# constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 750

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
        # width = 100
        # height = 50

        # x = SCREEN_WIDTH/2 - width
        # y = SCREEN_HEIGHT/2 - height

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
        
        py.draw.rect(screen, (3,180,255), self.button) 
        screen.blit(text,(x,y+height/8)) 
        
class taskInput : 

    def __init__(self):
        self.text = psg.popup_get_text("Task: ")
    
    def get(self): 
        return self.text
    
class textField: 
    
    def __init__(self, content,screen):
        self.content = content
        self.screen = screen 
        self.x = 50
        self.y = 50
        self.wrapLength = 200
        self.fontSize = 30

        self.font = py.font.SysFont("Arial", self.fontSize)

        self.border = py.rect.Rect(self.x,self.y,SCREEN_WIDTH-100,SCREEN_HEIGHT-100)
        py.draw.rect(self.screen, (255,255,255), self.border)

        text = self.font.render(self.content, True, (0,0,0), wraplength=self.wrapLength)
        self.screen.blit(text,(self.x,self.y))

    def change(self, tasks): 
        self.tasks = tasks
        content = self.content
        wrapLength = self.wrapLength

        new_tasks = []
        self.d_buttons = []

        moveDown = self.fontSize

        py.draw.rect(self.screen, (255,255,255), self.border)

        for lines in range(0,len(tasks)) : 
            self.d_buttons.append(button(self.screen,50,25,SCREEN_WIDTH-100,self.y,"done",15))
            self.d_buttons[len(self.d_buttons)-1].draw()

            text = self.font.render(tasks[lines][0], True, (0,0,0), wraplength=wrapLength)
            self.screen.blit(text,(self.x,self.y))

            new_tasks.append([tasks[lines][0],self.y])

            # if len(tasks[lines][0]) >= 6 :
            #     print(tasks[lines][0], " is too long")
            #     moveDown = 30 * round(len(tasks[lines][0]),1) % 6
            # else : 
            moveDown = 35 + round(len(tasks[lines][0]),1)

            self.y+=moveDown

        self.y = 50

        return new_tasks
        

py.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
s_color = (196,238,255)
screen.fill(s_color)

b_addTask = button(screen, 100, 50, SCREEN_WIDTH-150, SCREEN_HEIGHT-100,"+",30)
b_addTask.draw()
t_textField = textField("Add a new task!", screen)

tasks = []

py.display.flip()

while running : 

    for event in py.event.get() :
        if event.type == py.QUIT : 
            running = False; 

        if event.type == py.MOUSEBUTTONDOWN : 
            if b_addTask.button.collidepoint(event.pos) : 

                print("pressed")

                screen.fill(s_color)

                tasks.append([taskInput().get()])
                tasks = t_textField.change(tasks)
                print(tasks)

            if t_textField.border.collidepoint(event.pos) : 
                for i in range(0,len(t_textField.d_buttons)) :
                    if t_textField.d_buttons[i].button.collidepoint(event.pos) :
                        print(t_textField.d_buttons[i].y)
                        del tasks[i]
                        print(tasks)
                        tasks = t_textField.change(tasks)

                        break

    b_addTask.draw()
    py.display.update()
                                
