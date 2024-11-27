class Gamestate():
    def __init__(self,board):
        """self.board=[
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp' for i in range(8)],
            [' ' for i in range (8)],
            [' ' for i in range(8)],
            [' ' for i in range(8)],
            [' ' for i in range(8)],
            ['wp' for i in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']

        ]"""
        self.board=board

        self.movefunctions={'p':self.getPawnmoves,'R':self.getRookmoves,'Q':self.getQueenmoves,'N':self.getKnightmoves
            ,'K':self.getKingmoves,'B':self.getBishopmoves,'E':self.getElephantmoves,'C':self.getCanonmoves,'H':self.getKnightmoves,
                            'L':self.getRookmoves,'A':self.getAdvisormoves,'W':self.getXiangqipawnmoves}
        self.whitemove = True
        self.movlog=[]
        self.whitekinglocation=(len(self.board)-1,4)
        self.blackkinglocation=(0,4)
        self.checkmate=False
        self.stalemate=False
        self.enpassantpossible=()
        self.currentcastleright=CastleRights(True,True,True,True)
        self.castlerightlog=[CastleRights(self.currentcastleright.wks,self.currentcastleright.bks
                                             ,self.currentcastleright.wqs,self.currentcastleright.bqs)]

    def updatecastlerights(self, Move):
        if Move.piecemove=='wK':
            self.currentcastleright.wks=False
            self.currentcastleright.wqs=False
        elif Move.piecemove=='bK':
            self.currentcastleright.bks=False
            self.currentcastleright.bqs=False
        elif Move.piecemove=='wR':
            if Move.startrow==len(self.board)-1:
                if Move.startcol==0:
                    self.currentcastleright.wqs=False
                elif Move.startcol==len(self.board)-1:
                    self.currentcastleright.wks=False
        elif Move.piecemove == 'bR':
            if Move.startrow == 0:
                if Move.startcol == 0:
                    self.currentcastleright.bqs = False
                elif Move.startcol == len(self.board)-1:
                    self.currentcastleright.bks = False

    def Makemove(self,Move):
        self.board[Move.startrow][Move.startcol]=' '
        self.board[Move.endrow][Move.endcol]=Move.piecemove
        self.movlog.append((Move))
        self.whitemove=not self.whitemove
        if(Move.piecemove=='wK'):
            self.whitekinglocation=(Move.endrow,Move.endcol)
        elif Move.piecemove=='bK':
            self.blackkinglocation=(Move.endrow,Move.endcol)

        if Move.isapawnpromotion:
            self.board[Move.endrow][Move.endcol]=Move.piecemove[0]+'Q'
        if Move.isenpassantmove:
            self.board[Move.startrow][Move.endcol]=' '
        if abs(Move.endrow-Move.startrow)==2 and Move.piecemove[1]=='p' :
            self.enpassantpossible=((Move.startrow+Move.endrow)//2,Move.endcol)
        else:
            self.enpassantpossible=()

        if Move.iscastlemove:
            if Move.endcol-Move.startcol==2:
                self.board[Move.endrow][Move.endcol-1]=self.board[Move.endrow][Move.endcol+1]
                self.board[Move.endrow][Move.endcol+1]=' '

            else:
                self.board[Move.endrow][Move.endcol + 1] = self.board[Move.endrow][Move.endcol -2]
                self.board[Move.endrow][Move.endcol - 2] = ' '


        self.updatecastlerights(Move)
        self.castlerightlog.append(CastleRights(self.currentcastleright.wks, self.currentcastleright.bks
                                               , self.currentcastleright.wqs, self.currentcastleright.bqs))



    def Undomove(self):
        if(len(self.movlog)>0):
            Move= self.movlog.pop()
            self.board[Move.startrow][Move.startcol] = Move.piecemove
            self.board[Move.endrow][Move.endcol] = Move.piececaptured
            self.whitemove = not self.whitemove
            if(Move.piecemove=='wK'):
                self.whitekinglocation=(Move.startrow,Move.startcol)
            elif(Move.piecemove=='bK'):
                self.blackkinglocation=(Move.startrow,Move.startcol)
            if Move.isenpassantmove:
                self.board[Move.endrow][Move.endcol] = ' '
                self.board[Move.startrow][Move.endcol]=Move.piececaptured
                self.enpassantpossible=(Move.endrow,Move.endcol)
            if Move.piecemove[1]=='p' and abs(Move.startrow-Move.endrow)==2:
                self.enpassantpossible=()
            self.castlerightlog.pop()
            castlerights=self.castlerightlog[-1]
            self.currentcastleright=castlerights
            if Move.iscastlemove:
                if Move.endcol-Move.startcol==2:
                    self.board[Move.endrow][Move.endcol+1]=self.board[Move.endrow][Move.endcol-1]
                    self.board[Move.endrow][Move.endcol-1]=' '
                else:
                    self.board[Move.endrow][Move.endcol-2]=self.board[Move.endrow][Move.endcol+1]
                    self.board[Move.endrow][Move.endcol+1]=' '
        self.checkmate=False
        self.stalemate=False

    def getvalidmoves(self):

        tempcastlrightslog=self.castlerightlog
        tempenpassantpossible=self.enpassantpossible
        tempcastlerights=CastleRights(self.currentcastleright.wks, self.currentcastleright.bks
                                               , self.currentcastleright.wqs, self.currentcastleright.bqs)
        moves=self.getallpossiblemove()

        if self.whitemove:
            self.getcastlemoves(self.whitekinglocation[0],self.whitekinglocation[1],moves)
        else:
            self.getcastlemoves(self.blackkinglocation[0],self.blackkinglocation[1],moves)

        for i in range(len(moves)-1,-1,-1):
            self.Makemove(moves[i])
            self.whitemove=not self.whitemove

            if self.incheck():
                moves.remove(moves[i])
            self.whitemove=not self.whitemove
            self.Undomove()

        if (len(moves)) == 0:
            if self.incheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate=False
            self.stalemate=False
        self.castlerightlog=tempcastlrightslog
        self.currentcastleright=tempcastlerights
        self.enpassantpossible=tempenpassantpossible

        return moves
    def incheck(self):
        if self.whitemove:
            return self.squnderattack(self.whitekinglocation[0],self.whitekinglocation[1])
        else:
            return self.squnderattack(self.blackkinglocation[0],self.blackkinglocation[1])
    def squnderattack(self,i,j):

        self.whitemove=not self.whitemove
        validmoves=self.getallpossiblemove()
        self.whitemove = not self.whitemove
        for move in validmoves:
            if move.endrow==i and move.endcol==j:

                return True
        return False


    def getallpossiblemove(self):
        moves=[]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                turn=self.board[i][j][0]
                if(turn=='w'and self.whitemove)or (turn=='b'and not self.whitemove):
                    piece=self.board[i][j][1]
                    self.movefunctions[piece](i,j,moves)

        return moves

    def getPawnmoves(self,i,j,moves):
        if self.whitemove:
            if self.board[i-1][j]==' ':
                moves.append(Move((i,j),(i-1,j),self.board))
                if(i==len(self.board)-2 and self.board[i-2][j]==' '):
                    moves.append(Move((i,j),(i-2,j),self.board))
            if j-1>=0:
                if self.board[i-1][j-1][0]=='b':
                    moves.append(Move((i,j),(i-1,j-1),self.board))
                elif (i-1,j-1)==self.enpassantpossible:
                    moves.append(Move((i, j), (i - 1, j - 1), self.board, isenpassantmove=True))
            if j+1<=len(self.board)-1:
                if self.board[i-1][j+1][0]=='b':
                    moves.append(Move((i,j),(i-1,j+1),self.board))
                elif (i-1,j+1)==self.enpassantpossible:
                    moves.append(Move((i, j), (i - 1, j + 1), self.board, isenpassantmove=True))
        else:
            if self.board[i+1][j]==' ':
                moves.append(Move((i,j),(i+1,j),self.board))
                if(i==1 and self.board[i+2][j]==' '):
                    moves.append(Move((i,j),(i+2,j),self.board))
            if j-1>=0:
                if self.board[i+1][j-1][0]=='w':
                    moves.append(Move((i,j),(i+1,j-1),self.board))
                elif (i+1,j-1)==self.enpassantpossible:
                    moves.append(Move((i, j), (i + 1, j - 1), self.board, isenpassantmove=True))
            if j+1<=len(self.board)-1:
                if self.board[i+1][j+1][0]=='w':
                    moves.append(Move((i,j),(i+1,j+1),self.board))
                elif (i+1,j+1)==self.enpassantpossible:
                    moves.append(Move((i, j), (i + 1, j + 1), self.board, isenpassantmove=True))
    def getRookmoves(self,i,j,moves):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        opponent = 'b' if self.whitemove else 'w'
        for direction in directions:
            c = 1
            while 0 <= i + c * direction[0] <= len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]] == ' ':
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))
                c += 1
            if 0 <= i + c * direction[0] <=len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]][0] == opponent:
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))




    def getKnightmoves(self,i,j,moves):
        opponent='b' if self.whitemove else 'w'
        allycolor='w' if self.whitemove else 'b'
        indices=[1,-1,2,-2]
        directions=[(i,j) for i in indices for j in indices if abs(i)!=abs(j)]
        for dir in directions:
            if(0<=i+dir[0]<=len(self.board)-1 and 0<=j+dir[1]<=len(self.board)-1):
                   if self.board[i+dir[0]][j+dir[1]]==' 'or self.board[i+dir[0]][j+dir[1]][0]==opponent:
                       moves.append(Move((i,j),(i+dir[0],j+dir[1]),self.board))

    def getcastlemoves(self,i,j,moves):
        if self.squnderattack(i,j):
            return
        if (self.whitemove and self.currentcastleright.wks) or (not self.whitemove and self.currentcastleright.bks):
            self.getkingsidecastlemoves(i,j,moves)
        if(self.whitemove and self.currentcastleright.wqs) or (not self.whitemove and self.currentcastleright.bqs):
            self.getqueensidecastlemoves(i,j,moves)

    def getkingsidecastlemoves(self,i,j,moves):
        if self.board[i][j+1]==' ' and self.board[i][j+2]==' ':
            if not self.squnderattack(i,j+1) and not self.squnderattack(i,j+2):
                moves.append(Move((i,j),(i,j+2),self.board,iscastlemove=True))
    def getqueensidecastlemoves(self,i,j,moves):

        if self.board[i][j-1]==' ' and self.board[i][j-2]==' ' and self.board[i][j-3]==' ':
            if not self.squnderattack(i,j-1) and not self.squnderattack(i,j-2):
                moves.append(Move((i,j),(i,j-2),self.board,iscastlemove=True))
    def getBishopmoves(self,i,j,moves):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        opponent = 'b' if self.whitemove else 'w'
        for direction in directions:
            c = 1
            while 0 <= i + c * direction[0] <= len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]] == ' ':
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))
                c += 1
            if 0 <= i + c * direction[0] <= len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]][0] == opponent:
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))


    def getQueenmoves(self,i,j,moves):
        self.getBishopmoves(i,j,moves)
        self.getRookmoves(i,j,moves)
    def getKingmoves(self,i,j,moves):
        opponent = 'b' if self.whitemove else 'w'
        indices = [1,0, -1]
        directions = [(i, j) for i in indices for j in indices]
        for dir in directions:
            if (0 <= i + dir[0] <= len(self.board)-1 and 0 <= j + dir[1] <= len(self.board)-1):
                if (self.board[i + dir[0]][j + dir[1]] == ' ' ) or self.board[i + dir[0]][j + dir[1]][0] == opponent:
                    moves.append(Move((i, j), (i + dir[0], j + dir[1]), self.board))
    def getElephantmoves(self,i,j,moves):
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        opponent = 'b' if self.whitemove else 'w'
        for direction in directions:
            c = 1
            while 0 <= i + c * direction[0] <= len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]] == ' ' and c<=2:
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))
                c += 1
            if 0 <= i + c * direction[0] <= len(self.board)-1 and 0 <= j + c * direction[1] <= len(self.board)-1 and \
                    self.board[i + c * direction[0]][j + c * direction[1]][0] == opponent:
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))

    def getCanonmoves(self,i,j,moves):
        directions=[(1,0),(0,1),(-1,0),(0,-1)]
        opponent='b' if self.whitemove else 'w'
        for direction in directions:
            c=1
            while 0<=i+c*direction[0]<=7 and 0<=j+c*direction[1]<=7 and self.board[i+c*direction[0]][j+c*direction[1]]==' ':
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))
                c+=1
            c+=1
            while 0<=i+c*direction[0]<=7 and 0<=j+c*direction[1]<=7 and self.board[i+c*direction[0]][j+c*direction[1]]==' ':

                c+=1
            if 0 <= i + c * direction[0] <= 7 and 0 <= j + c * direction[1] <= 7 and \
                    self.board[i + c * direction[0]][j + c * direction[1]][0] == opponent:
                moves.append(Move((i, j), (i + c * direction[0], j + c * direction[1]), self.board))

    def getAdvisormoves(self,i,j,moves):
        opponent = 'b' if self.whitemove else 'w'
        indices = [1, 0, -1]
        directions = [(i, j) for i in indices for j in indices]
        for dir in directions:
            if self.whitemove:
                if (6 <= i + dir[0] <= 8 and 3 <= j + dir[1] <= 5):
                    if self.board[i + dir[0]][j + dir[1]] == ' ' or self.board[i + dir[0]][j + dir[1]][0] == opponent:
                        moves.append(Move((i, j), (i + dir[0], j + dir[1]), self.board))
            else:
                if (0 <= i + dir[0] <= 2 and 3 <= j + dir[1] <= 5):
                    if self.board[i + dir[0]][j + dir[1]] == ' ' or self.board[i + dir[0]][j + dir[1]][0] == opponent:
                        moves.append(Move((i, j), (i + dir[0], j + dir[1]), self.board))
    def getXiangqipawnmoves(self,i,j,moves):
        if self.whitemove:
            if  4<=i<=len(self.board)-1:
                if i-1>=0 and  (self.board[i-1][j]==" " or self.board[i-1][j][0]=='b'):
                    moves.append(Move((i,j),(i-1,j),self.board))
            elif 0<i<=4:
                if i-1>=0 and (self.board[i-1][j]==" " or self.board[i-1][j][0]=='b'):
                    moves.append(Move((i,j),(i-1,j),self.board))
                if j-1>=0  and (self.board[i][j-1]==" " or self.board[i][j-1][0]=='b'):
                    moves.append(Move((i,j),(i,j-1),self.board))
                if j+1<=len(self.board)-1  and (self.board[i][j+1]==" " or self.board[i][j+1][0]=='b'):
                    moves.append(Move((i,j),(i,j+1),self.board))
        else:
            if i<=4:
                if i+1<=len(self.board)-1 and  (self.board[i+1][j]==" " or self.board[i+1][j][0]=='b'):
                    moves.append(Move((i,j),(i+1,j),self.board))
            elif 4<i<=len(self.board)-1:
                if i+1<=len(self.board)-1 and (self.board[i+1][j]==" " or self.board[i+1][j][0]=='b'):
                    moves.append(Move((i,j),(i+1,j),self.board))
                if j-1>=0  and self.board[i][j-1]==" " or self.board[i][j-1][0]=='b':
                    moves.append(Move((i,j),(i,j-1),self.board))
                if j+1<=len(self.board)-1  and (self.board[i][j+1]==" " or self.board[i][j+1][0]=='b'):
                    moves.append(Move((i,j),(i,j+1),self.board))

    def printboard(self):
        print(self.board)
class Move():
    def __init__(self, startsq, endsq, board, isenpassantmove=False,iscastlemove=False):
        self.startrow=startsq[0]
        self.startcol=startsq[1]
        self.endrow=endsq[0]
        self.endcol=endsq[1]
        self.piecemove=board[self.startrow][self.startcol]
        self.piececaptured=board[self.endrow][self.endcol]
        self.moveID=self.startrow*1000+self.startcol*100+self.endrow*10+self.endcol
        self.isapawnpromotion=False
        self.isenpassantmove=False
        if(self.piecemove=='wp' and self.endrow==0)or (self.piecemove=='bp' and self.endrow==board):
            self.isapawnpromotion=True

        self.isenpassantmove=isenpassantmove
        if self.isenpassantmove:
            self.piececaptured='wp' if self.piecemove=='bp' else 'bp'
        self.iscastlemove=iscastlemove

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False
class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs


