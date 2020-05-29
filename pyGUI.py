import pygame
import GUI

class Window():
    def __init__(self):
        pygame.init()
        #Constants
        self.display_width = 1280
        self.display_heigth = 720
        
        #Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (186, 18 ,0)
        self.btn = (157, 209, 241)
        self.highlight_btn = (200, 224, 244)
        
        #Fonts
        self.font = pygame.font.SysFont("comicsans", 40)
        self.font_small = pygame.font.SysFont("comicsans", 24)        
        
        #Scenes
        self.alert = True
        
        self.window = pygame.display.set_mode((self.display_width, self.display_heigth))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.alertPage()
        
    def alertPage(self):
        
        while self.alert:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.redrawAlert()
            pygame.display.update()
            self.clock.tick(60)
            
    def loginPage(self):
        pygame.quit()
        GUI.main()
            
    def redrawAlert(self):
        self.window.fill(self.white)
        text = "WARNING: This is an Alpha program! Use at your own risk!"
        TextSurf, TextRect = self.text_objects(text, self.font, self.black)
        TextRect.center = ((self.display_width/2), (self.display_heigth/2))
        self.window.blit(TextSurf, TextRect)
        self.button(self.window, "Agree", self.font, 150, 455, 300, 80, self.btn, self.highlight_btn, self.loginPage)
        self.button(self.window, "Disagree", self.font, 825, 455, 300, 80, self.btn, self.highlight_btn, quit)
        
    def text_objects(self, text, font, color):
        textSurface = font.render(text, 1, color)
        return textSurface, textSurface.get_rect()

    def button(self, window, msg, font, x,y,w,h,ic,ac, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        textSurf, textRect = self.text_objects(msg, font, self.black)
        textRect.center = ( (x+(w/2), y+(h/2)) )
        window.blit(textSurf, textRect)
    
pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont("comicsans", 32)
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    Window()
    #main()
    pygame.quit()
    quit()