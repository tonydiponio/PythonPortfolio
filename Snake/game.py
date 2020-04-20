###############################################################################
# Tony DiPonio
# SNAKE
# Apr 2020
###############################################################################

import pygame
import random

pygame.init()

# Name the window
pygame.display.set_caption('Snake')
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

# Play background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


###############################################################################
# Define and initilize Variables
###############################################################################

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 120, 0)
blue = (0, 0, 255)

# global screen_width
screen_width = 800
screen_height = 600
appleThickness = 30
block_size = 20

direction = "right"

# Apple bite sound effect
appleSound = pygame.mixer.Sound('apple.wav')

# Define different fonts
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

# Setup the game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the graphic images
img = pygame.image.load('snakeHead.png')
apple = pygame.image.load('apple.png')

clock = pygame.time.Clock()

###############################################################################
# Define Functions
###############################################################################


def pause():
    paused = True
    message_to_screen("Game is Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit", black, 25)
    pygame.display.update()
    clock.tick(5)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    screen.blit(text, [0, 0])


def highscore(highscore):
    text = smallfont.render("Best: " + str(highscore), True, black)
    screen.blit(text, [screen_width-100, 0])


# Read the high score from the text file
def readHS():
    f = open('highscore.txt', 'r')
    HS = f.readline()
    f.close()
    if HS != "" and HS != 0 and HS != "0":
        return HS
    else:
        return "1"


# Write the high score to the text file
def writeHS(HS):
    string = str(HS)
    f = open('highscore.txt', 'w')
    f.write(string)
    f.close()


def randAppleGen():
    randApplex = round(random.randrange(0, screen_width - appleThickness))  # /appleThickness)*appleThickness
    randAppley = round(random.randrange(0, screen_height - appleThickness))  # /appleThickness)*appleThickness

    return randApplex, randAppley


# Show the intro screen onec when game is started
def game_intro():
    screen.fill(white)
    message_to_screen("Welcome to Snake", green, -100, "med")
    message_to_screen("The objective of this game is to eat red apples.", black, -30)
    message_to_screen("The more apples you eat the longer you get.", black, 0)
    message_to_screen("If you run into the edge of the screen or yourself, You Die!", black, 30)
    message_to_screen("Press C to play, SPACE to pause, or Q to quit:", black, 80)

    pygame.display.update()

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


# Draw the snake
def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)
    elif direction == "up":
        head = img

    screen.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(screen, green, [XnY[0], XnY[1], block_size, block_size])


def text_objects(text, colour, size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    elif size == "med":
        textSurface = medfont.render(text, True, colour)
    elif size == "large":
        textSurface = largefont.render(text, True, colour)

    return textSurface, textSurface.get_rect()


# Output message text to screen
def message_to_screen(msg, colour, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (screen_width/2), (screen_height/2) + y_displace
    screen.blit(textSurf, textRect)


# Main game loop function
def gameLoop():
    global direction
    direction = "right"
    global bestScore

    gameEnd = False
    gameOver = False
    FPS = 10

    lead_x = screen_width/2
    lead_y = screen_height/2
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randApplex, randAppley = randAppleGen()

    while not gameEnd:

        if gameOver is True:
            message_to_screen("Game Over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to Quit", black, 20, size="small")
            pygame.display.update()

        while gameOver is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameEnd = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameEnd = True
                    elif event.key == pygame.K_c:
                        gameLoop()

        # Check user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameEnd = True
            if event.type == pygame.KEYDOWN:
                if direction != "right" and event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif direction != "left" and event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif direction != "down" and event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif direction != "up" and event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_SPACE:
                    pause()

        # Check screen boundaries for game over
        if lead_x >= screen_width or lead_x < 0 or lead_y >= screen_height or lead_y < 0:
            gameOver = True

        # Calculate motion of snake
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Fill the background
        screen.fill(white)

        # Draw the Apple
        screen.blit(apple, [randApplex, randAppley, appleThickness, appleThickness])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        # Check if the list is longer than the snake is supposed to be
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Check for snakeHead collision with body
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        # Draw the snake
        snake(block_size, snakeList)

        # Call the score function
        score(snakeLength-1)

        # Check for high score
        if snakeLength-1 > bestScore:
            bestScore = snakeLength-1
            writeHS(bestScore)

        # Call the score function
        highscore(bestScore)

        # Update the display
        pygame.display.update()

        # Check for collision with an Apple
        if lead_x > randApplex and lead_x < randApplex + appleThickness or (lead_x + block_size) > randApplex and (lead_x + block_size) < randApplex + appleThickness:
            if lead_y >= randAppley and lead_y < randAppley + appleThickness or (lead_y + block_size) > randAppley and (lead_y + block_size) < randAppley + appleThickness:

                randApplex, randAppley = randAppleGen()
                snakeLength += 1
                FPS += 1
                appleSound.play()

        clock.tick(FPS)

    # Done.  Time to quit
    pygame.quit()
    exit()


###############################################################################
# Call Functions
###############################################################################

# Initilize the High Score from the saved text file
bestScore = int(readHS())

game_intro()
gameLoop()
