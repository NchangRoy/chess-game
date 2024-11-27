import random
import random as r
piecescores={'K':0,'Q':10,'R':5,'B':3,'N':3,'p':1,'E':3,'C':5,'H':3,'L':10,'W':1,'A':3}
Checkmate=1000
stalemate=0
Depth=1

def findrandmove(validmoves):
    return validmoves[r.randint(0,len(validmoves)-1)]
"""def findbestmove(validmoves,gs):

    turnmultiplier=1 if gs.whitemove else -1
    opponenentminmaxscore=Checkmate
    bestmove=None
    maxscore=-Checkmate #black perspective
    r.shuffle(validmoves)
    for playermove in validmoves:
        gs.Makemove(playermove)
        opponentMoves=gs.getvalidmoves()

        opponenentmaxscore=-Checkmate
        for opponentmove in opponentMoves:
            gs.Makemove(opponentmove)

            if gs.checkmate:
                score=Checkmate
            elif gs.stalemate:
                score=stalemate
            score=-scorematerial(gs.board)*turnmultiplier

            if score >opponenentmaxscore:
                opponenentmaxscore=score

            gs.Undomove()
        if opponenentminmaxscore>opponenentmaxscore:
            opponenentminmaxscore=opponenentmaxscore
            bestmove = playermove
        gs.Undomove()
    return bestmove

"""
def scorematerial(board):
    score=0
    for row in board:
        for square in row:
            if square[0]=='w':
                score+=piecescores[square[1]]
            elif square[0]=='b':
                score-=piecescores[square[1]]
    return score

def findbestmove(gs, validmoves):
    global  nextmove
    nextmove=None
    findmoveminmax(gs,validmoves,Depth,gs.whitemove)

    return nextmove
def scoreboard(gs):
    if gs.checkmate:
        if gs.whitemove:
            return -Checkmate
        else:
            return Checkmate
    elif gs.stalemate:
        return stalemate
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piecescores[square[1]]
            elif square[0] == 'b':
                score -= piecescores[square[1]]
    return score
def findmoveminmax(gs,validmoves,depth,whitemove):

    global nextmove
    if depth==0:
        return scoreboard(gs)
    if whitemove:
        maxscore=-Checkmate
        for move in validmoves:
            gs.Makemove(move)
            nextmoves=gs.getvalidmoves()
            score=findmoveminmax(gs,nextmoves,depth-1,False)
            if score>maxscore:
                maxscore=score
                if depth==Depth:
                    nextmove=move
            gs.Undomove()
            return  maxscore

    else:
        minscore=Checkmate
        for move in validmoves:
            gs.Makemove(move)
            nextmoves=gs.getvalidmoves()
            score=findmoveminmax(gs,nextmoves,depth-1,True)
            if score<minscore:
                minscore=score
                if depth==Depth:
                    nextmove=move
            gs.Undomove()
            return minscore

def findmoveNegamax(gs,validmoves,depth,turnmultiplier):
    global nextmove

    if depth==0:
        return turnmultiplier*scoreboard(gs)
    maxscore=-Checkmate
    for move in validmoves:
        gs.Makemove(move)
        nextmoves=gs.getvalidmoves()
        score=-findmoveNegamax(gs,nextmoves,depth-1,-turnmultiplier)
        if score>maxscore:
            maxscore=score
            if depth==Depth:
                nextmove=move
        gs.Undomove()
    return maxscore
def findbestmoveNegamax(gs,validmoves):
    global nextmove,counter
    nextmove=None
    counter=0
    random.shuffle(validmoves)
    findmoveNegamaxAlphaBeta(gs,validmoves,Depth,1 if gs.whitemove else -1,-Checkmate,Checkmate)
    print(counter)
    return nextmove
def findmoveNegamaxAlphaBeta(gs,validmoves,depth,turnmultiplier,alpha,beta):
    global nextmove,counter

    counter+=1
    if depth==0:
        return turnmultiplier*scoreboard(gs)

    maxscore=-Checkmate
    for move in validmoves:
        gs.Makemove(move)
        nextmoves=gs.getvalidmoves()
        score=-findmoveNegamaxAlphaBeta(gs,nextmoves,depth-1,-turnmultiplier,-beta,-alpha)
        if score>maxscore:
            maxscore=score
            if depth==Depth:
                nextmove=move
        gs.Undomove()
        if maxscore>alpha:
            alpha=maxscore
        if alpha>=beta:
            break
    return maxscore


