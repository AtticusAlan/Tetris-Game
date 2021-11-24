import sys 
import pygame 
import random 
import time

pygame.init()

# define color
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# define font
SMALL_FONT = pygame.font.SysFont("monospace", 20)

# all possible blocks to generate
blocks = [
    [[0,0],[0,1],[0,2],[0,3]],      # I shape
    [[0,0],[0,1],[1,0],[1,1]],      # O shape
    [[0,0],[1,0],[0,1],[0,2]],      # Z shape
    [[0,0],[1,0],[0,-1],[0,-2]],    # S shape
    [[0,0],[0,1],[1,1],[1,2]],      # T shape 
    [[0,0],[0,-1],[1,-1],[1,-2]],   # L shape   
    [[0,0],[0,1],[0,-1],[1,0]],     # J shape
]

# select random block from 7 shapes
select = list(random.choice(blocks))
# set initial position 
init_pos = [21, 5]

def drop_block(screen, bg, score):
    y, x = init_pos
    y -= 1
    for row, column in select:
        row += y 
        column += x
        if bg[row][column] == 1:
            break 
    else:
        init_pos.clear() 
        init_pos.extend([y, x])
        return 
    
    # Reinitialize
    y, x = init_pos 
    for row, column in select:
        row += y 
        column += x 
        bg[row][column] = 1
    complete_row = []

    for row in range(1, 21):
        # if row is filled with blocks
        if 0 not in bg[row]:
            complete_row.append(row)
    complete_row.sort(reverse=True)
    
    # delete the completed row in background, and append
    for row in complete_row:
        bg.pop(row)
        bg.append(list(0 for column in range(0, 10)))

    score[0] += len(complete_row)
    # show score in caption
    pygame.display.set_caption('Tetris  Score: ' + str(score[0]))
    select.clear()
    select.extend(list(random.choice(blocks)))
    init_pos.clear()
    init_pos.extend([20, 5])
    y, x = init_pos
    for row, column in select:
        row += y
        column += x 
        # if every row in backgound has blocks, 
        # meaning it reached to the top of the window
        if bg[row][column] == 1:
            endScreen(screen, score)

# draw each block
def draw_block(screen, bg):
    y, x = init_pos
    for row, column in select:
        row += y
        column += x 
        pygame.draw.rect(screen, ORANGE, (column * 30, 600 - row * 30, 28, 28))
    for row in range(1, 21):
        for column in range(0, 10): 
            if bg[row][column] == 1:
                pygame.draw.rect(screen, BLUE, (column * 30, 600 - row * 30, 28, 28))

# rotate block 
def rotate(bg):
    y, x = init_pos 
    rotate_pos = [(-column, row) for row, column in select]
    for row, column in rotate_pos:
        row += y 
        column += x 
        # ensure block stays in the window, check collision 
        if column < 0 or column > 9 or bg[row][column]:
            break 
    else:
        select.clear() 
        select.extend(rotate_pos)
        
# move block left or right
def move(d, bg):
    y, x = init_pos 
    x += d
    for row, column in select:
        row += y 
        column += x 
        # ensure block stays in the window, check collision 
        if column < 0 or column > 9 or bg[row][column]:
            break 
    else:
        init_pos.clear() 
        init_pos.extend([y, x])

def endScreen(screen, score):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                # Pause for 0.5 sec
                pygame.time.delay(500)
            
        totalScore = SMALL_FONT.render('Score: ' + str(score[0]), 1, RED)
        screen.blit(totalScore, (150 - (totalScore.get_width())//2, 150))
        playAgain = SMALL_FONT.render('Press ANY KEY to restart', 1, GREEN)
        screen.blit(playAgain, (150 - (playAgain.get_width())//2, 200))
        
        pygame.display.update()
        
    main()


def main():
    screen = pygame.display.set_mode((300, 600))
    timer = 0 
    score = [0]
    pygame.display.set_caption('Tetris  Score: ' + str(score[0]))
    # press to accelerate dropping speed
    press = False 
    
    bg = [[0 for column in range(0, 10)] for row in range(0, 22)]
    bg[0] = [1 for column in range(0, 10)]
    
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    press = True 
                if event.key == pygame.K_UP:
                    rotate(bg)
                if event.key == pygame.K_RIGHT:
                    move(1, bg)
                if event.key == pygame.K_LEFT:
                    move(-1, bg)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    press = False 
        
        if press:
            # speed up the dropping rate
            timer += 10
        if timer >= 50:
            drop_block(screen, bg, score)
            timer = 0 # reset timer
        else:
            # default dropping speed
            timer += 1
            
        draw_block(screen, bg)
        pygame.time.Clock().tick(200)
        # pygame.display.flip()
        pygame.display.update()
        
    pygame.display.quit()
    pygame.quit()
    sys.exit()
            
if __name__ == "__main__":
    main()