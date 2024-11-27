import pygame as p
import chessengine as chess
import chessai
import display
import  os



width=height=450
dimensin=9
sq_size=height//dimensin
max_fps=15
images={}
existing=os.path.exists('images/bK.png')
screen=p.display.set_mode((width,height))
boards= {'C&X': {'board':[
    ['bL', 'bH', 'bE', 'bA', 'bK', 'bA', 'bE', 'bH', 'bL'],
    [' ' for i in range(9)],
    [' ','bC',' ',' ',' ',' ',' ','bC',' '],
    ['bW',' ','bW',' ','bW',' ','bW',' ','bW'],

    [' ' for i in range(9)],
    [' ' for i in range(9)],
    [' ' for i in range(9)],
    ['wp' for i in range(9)],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wQ', 'wB', 'wN', 'wR']],

    'dimension':9
},
    'C&C':
        {'board':[
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp' for i in range(8)],
            [' ' for i in range(8)],
            [' ' for i in range(8)],
            [' ' for i in range(8)],
            [' ' for i in range(8)],
            ['wp' for i in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']],
        'dimension':8
        },
}
gamemode = None
side=None

def loadimages():
    pieces=['bB','wp','bK','bp','bN','bR','wH','bH','bQ','wR','wQ','wN','wB','wK','bE','wE','wC','bC','wL','bL','wA','bA','bW','wW']
    for piece in pieces:
        images[piece]=p.transform.scale(p.image.load('images/'+piece+'.png'),(sq_size,sq_size))
def main():
    p.init()

    clock=p.time.Clock()
    screen.fill(p.Color('white'))
    gs=chess.Gamestate(boards[gamemode.value]['board'])
    validmoves=gs.getvalidmoves()
    movemade=False ##flag variable
    gs.printboard()
    loadimages()
    animate=False
    running=True
    sqselected=()
    playwerclick=[]
    gameover=False

    if side!=None:
        if side.value=='White':
            playerone=True
            playertwo=True
        elif side.value =='Black':
            playerone=False
            playertwo=False
        elif side.value=='CvsC':
            playerone=False
            playertwo=True
        elif side.value=='HvsH':
            playerone=True
            playertwo=False
    greedy=True

    while running:

        if side.value=='White':
            humanturn=gs.whitemove
        elif(side.value=='Black'):
            humanturn=not gs.whitemove


        if(side.value=='CvsC' or side.value=='HvsH'):
            if gs.whitemove==True:
                if playerone==True:
                    humanturn=True
                else :
                    humanturn=False
            else:
                if playertwo==False:
                    humanturn=True
                else:
                    humanturn=False
        #humanturn=(gs.whitemove and playerone)or (not gs.whitemove and not playertwo)
        """print(gs.whitemove and playerone)
        print(gs.whitemove)"""
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameover and humanturn:
                    location=p.mouse.get_pos()
                    col=location[0]//sq_size
                    row=location[1]//sq_size
                    if sqselected==(row,col):
                        sqselected=()
                        playwerclick=[]
                    else:
                        sqselected=(row,col)
                        playwerclick.append(sqselected)
                    if(len(playwerclick)==2):
                        move=chess.Move(playwerclick[0],playwerclick[1],gs.board)
                        for i  in range(len(validmoves)):
                            if move == validmoves[i]:

                                print('working')
                                animate=True
                                gs.Makemove(validmoves[i])
                                movemade=True
                                sqselected=()
                                playwerclick=[]
                        if not movemade:
                            playwerclick=[sqselected]
                    else:
                        moves=gs.getvalidmoves()

            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.Undomove()
                    movemade=True
                    animate=False
                if e.key==p.K_r:
                    gs=chess.Gamestate(gamemode.value)
                    validmoves=gs.getvalidmoves()
                    sqselected=()
                    playwerclick=[]
                    movemade=False
                    animate=False
            #ai movement
            if not gameover and not humanturn:
                AImove=chessai.findbestmoveNegamax(gs,validmoves)
                if AImove is None:
                    greedy=False
                    AImove=chessai.findrandmove(validmoves)
                print(gs.whitemove)
                
                gs.Makemove(AImove)
               
                movemade=True
                animate=True
               

            if movemade:
                if animate:
                    animatemove(gs.movlog[-1],screen,gs.board,clock)
                validmoves=gs.getvalidmoves()
                movemade=False
                animate=False

            drawgamestate(screen,gs,validmoves,sqselected)

            if gs.checkmate:
                gameover=True
                if gs.whitemove:
                    drawText(screen,'Black wins by Checkmate')
                else:
                    drawText(screen,'White wins by checkmate')
            elif gs.stalemate:
                drawText(screen,'Stalemate')
            clock.tick(max_fps)
            p.display.flip()

def drawredtile(screen,position):
    color=p.Color('Red')
    p.draw.rect(screen, color, p.Rect(position[1] * sq_size, position[0] * sq_size, sq_size, sq_size))


def drawtextat(screen,text,x,y):
    font=p.font.SysFont('arialblack',15)
    color=p.Color('black')
    textobject=font.render(text,True,color)
    screen.blit(textobject,(x,y))
def drawgamestate(screen,gs,validmoves,sqselected):
    drawboard(screen)
    if gs.incheck():
        if gs.squnderattack(gs.whitekinglocation[0], gs.whitekinglocation[1]):
            drawredtile(screen, (gs.whitekinglocation[0], gs.whitekinglocation[1]))
        elif gs.squnderattack(gs.blackkinglocation[0], gs.blackkinglocation[1]):
            drawredtile(screen, (gs.blackkinglocation[0], gs.blackkinglocation[1]))
    highlightsquares(screen,gs,validmoves,sqselected)
    drawpieces(screen,gs.board)

def drawText(screen,text):
    font=p.font.SysFont('Arial',32)
    textobject=font.render(text,0,p.Color('Black'))
    textlocation=p.Rect(0,0,width,height).move(width/2-textobject.get_width()/2,height/2-textobject.get_height()/2)
    screen.blit(textobject,textlocation)

def drawboard(screen):
    global colors
    colors=[p.Color('white'),p.Color('grey')]
    for i in range(len(boards[gamemode.value]['board'])):
        for j in range(len(boards[gamemode.value]['board'])):
            color=colors[(i+j)%2]
            p.draw.rect(screen,color,p.Rect(j*sq_size,i*sq_size,sq_size,sq_size))

def drawpieces(screen,board):
    for i in range(len(boards[gamemode.value]['board'])):
        for j in range(len(boards[gamemode.value]['board'])):
            piece=board[i][j]
            if(piece!=' '):
                screen.blit(images[piece],p.Rect(j*sq_size,i*sq_size,sq_size,sq_size))
    pass
def animatemove(move,screen,board,clock):
    coords=[]
    ChangeRow=move.endrow-move.startrow
    changecol=move.endcol-move.startcol
    framespersq=10
    framecount=(abs(changecol)+abs(ChangeRow))*framespersq
    for frame in range(framecount+1):
        i,j=(move.startrow+ChangeRow*(frame/framecount),move.startcol+changecol*(frame/framecount))
        drawboard(screen)
        drawpieces(screen,board)
        color=colors[(move.endrow+move.endcol)%2]
        endsq=p.Rect(move.endcol*sq_size,move.endrow*sq_size,sq_size,sq_size)
        p.draw.rect(screen,color,endsq)
        if move.piececaptured!=' ':
            screen.blit(images[move.piececaptured],endsq)

        screen.blit(images[move.piecemove],p.Rect(j*sq_size,i*sq_size,sq_size,sq_size))
        p.display.flip()
        clock.tick(60)

def highlightsquares(screen,gs,validmoves,sqselected):
    if sqselected!=():
        i,j=sqselected
        if gs.board[i][j][0]==('w' if gs.whitemove else 'b'):
            s=p.Surface((sq_size,sq_size))
            s.set_alpha(100)
            s.fill(p.Color('Blue'))
            screen.blit(s,(j*sq_size,i*sq_size))
            s.fill(p.Color('Green'))
            for move in validmoves:
                if move.startrow==i and move.startcol==j:
                    screen.blit(s,(move.endcol*sq_size,move.endrow*sq_size))
#main()
def settuppage():
    p.init()
    screen.fill(p.Color('white'))
    running=True
    global  gamemode
    gamemode=None
    global side
    side=None
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False

            else:
                button1=display.Button(screen,'play',20, 20,'Play')
                #buttons for move
                button2=display.Button(screen,'Chess & Chess',20,70,'C&C')
                button3=display.Button(screen,'Chess & Shogi',20, 100,'C&S')
                button9=display.Button(screen,'Chess & Xiangqi',20,160,'C&X')
                button4=display.Button(screen,'Xiangqi & Shogi',20, 130,'X&S')
                #buttons for color
                button5 = display.Button(screen, 'White', 20, 210, 'White')
                button6 = display.Button(screen, 'Black', 20, 240, 'Black')
                button7 = display.Button(screen, 'Computer vs Computer', 20, 270, 'CvsC')
                button8=display.Button(screen,'Human vs Human',20,300,'HvsH')

                button1.drawbutton()
                drawtextat(screen,'Choose your mode to play',20,50)
                button2.drawbutton()
                button3.drawbutton()
                button4.drawbutton()
                button9.drawbutton()
                drawtextat(screen,'Choose side',20,180)
                button5.drawbutton()
                button6.drawbutton()
                button7.drawbutton()
                button8.drawbutton()


                movebuttons=[button2,button3,button4,button9]
                for button in movebuttons:
                    if button.clicked:
                        if gamemode!=None:
                            rectangle=p.Rect(gamemode.x+gamemode.textobject.get_width()+10,gamemode.y,
                                             gamemode.textobject.get_height(),gamemode.textobject.get_height(),)
                            p.draw.rect(screen,p.Color('white'),rectangle)
                        gamemode=button




                sidebuttons=[button5,button6,button7,button8]
                for button in sidebuttons:
                    if button.clicked:
                        if side!=None:
                            rectangle=p.Rect(side.x+side.textobject.get_width()+10,side.y,
                                             side.textobject.get_height(),side.textobject.get_height(),)
                            p.draw.rect(screen,p.Color('white'),rectangle)
                        side=button


                if gamemode!=None :
                        screen.blit(gamemode.imagerect,(gamemode.x+gamemode.textobject.get_width()+10,gamemode.y))
                if side!=None:
                        screen.blit(side.imagerect,(side.x+side.textobject.get_width()+10,side.y))


                if button1.clicked and gamemode!=None:
                        print(gamemode.value)
                        main()

        p.display.update()

settuppage()


