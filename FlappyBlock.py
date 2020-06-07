# A small project with the goal of creating a clone of the popular game 
# Flappy Bird using python and the pygame and random libraries.
# Created by: Stephen Chen
# Date: 5/28/20

import os, pygame, random

class Player:
    y = 50
    x = 40
    vel = 0
    flyAccel = 7
    playerColor = (201,104,58)

    def PlayerController(self,game):
        if (self.vel < 5):
            self.vel += game.gravity
        self.y += self.vel
        if (self.y < 0 or self.y > game.ySize):
            game.gameOver = True

    def DrawPlayer(self,game):
        pygame.draw.rect(game.surface,(0,0,0),[int(self.x-5),int(self.y-5),10,10])
        pygame.draw.rect(game.surface,self.playerColor,[int(self.x-4),int(self.y-4),8,8])

    def PlayerFly(self,event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                self.vel -= self.flyAccel

class Pipe:
    def __init__(self,game):
        self.x = game.xSize + 100
        self.openingSize = 100
        self.openingHeight = random.randint(80,320)
        self.colorx = random.randint(1,3)
        self.colors = {1:(255,0,0),2:(0,255,0),3:(0,0,255)}
        self.color = self.colors[self.colorx]
        self.pipeTimer = 130
        self.spawn = False
        self.point = False
        self.speed = 1.5
    
    def DrawPipe(self,game):
        pygame.draw.rect(game.surface,(0,0,0),[int(self.x-25),0,50,int(self.openingHeight-self.openingSize/2)])
        pygame.draw.rect(game.surface,(0,0,0),[int(self.x-25),int(self.openingHeight+self.openingSize/2),50,(game.ySize-int(self.openingHeight-self.openingSize/2))])
        pygame.draw.rect(game.surface,self.color,[int(self.x-24),0,48,int(self.openingHeight-self.openingSize/2)-1])
        pygame.draw.rect(game.surface,self.color,[int(self.x-24),int(self.openingHeight+self.openingSize/2)+1,48,(game.ySize-int(self.openingHeight-self.openingSize/2))])

class Game:
    xSize = 300
    ySize = 400
    surface = pygame.display.set_mode((xSize,ySize))
    gameTimer = 0
    bgcolor = (80, 224, 235)
    gameOver = False
    points = 0
    gravity = 0.2
    gamedOver = False

class ScoreDisp:
    def __init__(self,game):
        self.scoreFont = pygame.font.Font('freesansbold.ttf', 13)
        self.scoreText = self.scoreFont.render(' Score: '+str(int(game.points/78))+' ',True,(0,0,0), (255,255,255))
        self.scoreTextRect = self.scoreText.get_rect()
        self.scoreTextRect.center = (40,40)

def QuitGame(event):
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                os._exit(1)

def PipeManager(pipeList,game):
    for pipe in pipeList:
        if (pipe.x < -100):
            pipeList.remove(pipe)
        if (pipe.pipeTimer == 0 and pipe.spawn == False):
            newPipe = Pipe(game)
            pipeList.append(newPipe)
            pipe.spawn = True
        pipe.DrawPipe(game)
        pipe.pipeTimer -= 1
        pipe.x -= pipe.speed

def CheckCollision(player,pipeList,game):
    for pipe in pipeList:
        if (pipe.x < player.x and pipe.point == False):
            pipe.point = True
            game.points += 1
        if (pipe.x-25 < player.x and pipe.x+25 > player.x):
            if (player.y < pipe.openingHeight-(pipe.openingSize/2-1)) or (player.y > pipe.openingHeight+(pipe.openingSize/2-1)):
                game.gameOver = True

def UpdateScore(score,game):
    score.scoreText = score.scoreFont.render(' Score: '+str(int(game.points))+' ',True,(0,0,0), (255,255,255))
    score.scoreTextRect = score.scoreText.get_rect()
    score.scoreTextRect.center = (40,40)

def GameOver():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 30)
    gameOverText = gameOverFont.render('Game Over', True, (0,0,0), game.bgcolor) 
    gameOverTextRect = gameOverText.get_rect()  
    gameOverTextRect.center = (game.xSize // 2, game.ySize // 3)

    restartFont = pygame.font.Font('freesansbold.ttf', 22)
    restartText = restartFont.render('Press Enter to Restart', True, (0,0,0), game.bgcolor) 
    restartTextRect = restartText.get_rect()  
    restartTextRect.center = (game.xSize // 2, (2*game.ySize) // 3)

    gameOverScoreFont = pygame.font.Font('freesansbold.ttf', 26)
    gameOverScoreText = gameOverScoreFont.render(' Score: '+str(game.points)+' ', True, (0,0,0), game.bgcolor) 
    gameOverScoreTextRect = gameOverScoreText.get_rect()  
    gameOverScoreTextRect.center = (game.xSize // 2, game.ySize // 2)

    pygame.draw.rect(game.surface,game.bgcolor,[0,0,game.xSize,game.ySize])
    player.DrawPlayer(game)
    PipeManager(pipeList,game)
    game.surface.blit(gameOverText, gameOverTextRect)
    game.surface.blit(restartText, restartTextRect)
    game.surface.blit(gameOverScoreText, gameOverScoreTextRect)
    pygame.display.update()
    game.gamedOver = True

pygame.init()
pygame.display.set_caption('Flappy Block')
player = Player()
game = Game()
score = ScoreDisp(game)
clock = pygame.time.Clock()
pipeList = []

while True:
    pygame.draw.rect(game.surface,game.bgcolor,[0,0,game.xSize,game.ySize])
    
    player.PlayerController(game)

    for event in pygame.event.get():                                                                                                    
        QuitGame(event)
        player.PlayerFly(event)
        if (game.gameOver == True):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player = Player()
                game = Game()
                score = ScoreDisp(game)
                pipeList = []
    
    if (game.gameTimer > 150):
        if (pipeList == []):
            pipe = Pipe(game)
            pipeList.append(pipe)
    PipeManager(pipeList,game)
    player.DrawPlayer(game)
    CheckCollision(player,pipeList,game)
    UpdateScore(score,game)
    game.surface.blit(score.scoreText,score.scoreTextRect)
    game.gameTimer += 1
    if (game.gameOver == False):
        pygame.display.update()
    if (game.gameOver == True and game.gamedOver == False):
        GameOver()
    clock.tick(60)

