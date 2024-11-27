import pygame as p
class Button():
    def __init__(self,screen,text,x,y,value):
        self.text=text
        self.value=value
        self.x=x
        self.y=y
        self.screen=screen
        self.font = p.font.SysFont('arialblack', 20)
        self.textobject = self.font.render(self.text, True, p.Color('Green'), p.Color('Red'))

        self.clicked=False
        self.imagerect = p.transform.scale(p.image.load('images/bQ.png'),
                                      (self.textobject.get_height(), self.textobject.get_height()))
        self.rectangle = p.Rect(self.x, self.y, self.textobject.get_width(), self.textobject.get_height())
    def drawbutton(self):


        mouselocaton=p.mouse.get_pos()
        if self.rectangle.collidepoint(mouselocaton):

            if p.mouse.get_pressed()[0]:
                self.clicked=True


        p.draw.rect(self.screen,p.Color('Yellow'),self.rectangle)
        self.screen.blit(self.textobject, (self.x,self.y))

