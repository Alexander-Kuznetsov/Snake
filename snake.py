from tkinter import *
import random

UP 	  = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3

class Pairs:
	x1, x2, y1, y2 = 0, 0, 0, 0

class Snake:
	max_size = 10
	route = UP
	body = []

class Fruit:
	count = 0
	pairs = Pairs()


SIZE_W, SIZE_H = 500, 500
X_START, Y_START = 240, 240
STEP = 20
SCORE = 0

root = Tk()
root.geometry('500x550')
root.title("Snake")

field = Canvas(root, width = SIZE_W, height = SIZE_H, bg = 'lightblue')
field.place(in_ = root, x = 0, y = 0)

btn = Button(root, text = "Start")
btn.pack() 

snake = Snake()
fruit = Fruit()

def onLeft(event):
	global snake
	if (snake.route != RIGHT):
		snake.route = LEFT

def onRight(event):
	global snake
	if (snake.route != LEFT):
		snake.route = RIGHT

def onUp(event):
	global snake
	if (snake.route != DOWN):
		snake.route = UP

def onDown(event):
	global snake
	if (snake.route != UP):
		snake.route = DOWN
 
def crashed(body):
	global SIZE_H, SIZE_W

	if (body.x1 < 0 or body.y1 < 0 or SIZE_H < body.y2 or SIZE_W < body.x2):
		return True
	return False

def getResult():
	global SIZE_H, SIZE_W
	global SCORE

	field.create_text(SIZE_H / 2, SIZE_W / 2, 
		text='YOU LOSE\n score: ' + str(SCORE), fill='red', font = 30)

def drawMap(snake, fruit):
	field.delete(ALL)
	drawSnake(snake.body)
	drawFruit(fruit.pairs)

def drawSnake(body):
	field.create_rectangle(body[0].x1, body[0].y1,
		 			body[0].x2, body[0].y2, fill="green")
	for i in range(1, len(body)):
		field.create_rectangle(body[i].x1, body[i].y1,
		 			body[i].x2, body[i].y2, fill="blue")

def drawFruit(pairs):
	if (pairs.x1 != None):
		field.create_oval(pairs.x1, pairs.y1,
		 			pairs.x2, pairs.y2, fill="red")

def eatFruit(snakePairs, fruitPairs, count):
	global SCORE

	if (count == 0 or snakePairs.x1 == None):
		return False

	if (snakePairs.x1 == fruitPairs.x1 and snakePairs.x2 == fruitPairs.x2
		and snakePairs.y1 == fruitPairs.y1 and snakePairs.y2 == fruitPairs.y2):
			SCORE += 10
			return True
	return False

def getFruit(snake, fruit):
	if (fruit.count == 0):
		x = random.randrange(0, (SIZE_W - STEP + 1), STEP)
		y = random.randrange(0, (SIZE_H - STEP + 1), STEP)
	else:
		return 0

	collision = False
	for i in range(len(snake.body)):
		if (snake.body[i].x1 == x or snake.body[i].y1 == y):
			collision = True
		if (collision == True):
			x = random.randrange(0, (SIZE_W - STEP + 1), STEP)
			y = random.randrange(0, (SIZE_H - STEP + 1), STEP)
			collision = False
			i = 0

	fruit.pairs.x1, fruit.pairs.y1 = x, y
	fruit.pairs.x2, fruit.pairs.y2 = x + STEP, y + STEP
	fruit.count += 1	

def riseSnake(snake):
	if (len(snake.body) < snake.max_size):
		pairs = Pairs()
		pairs.x1, pairs.y1 = snake.body[0].x1, snake.body[0].y1
		pairs.x2, pairs.y2 = snake.body[0].x2, snake.body[0].y2 
		snake.body.append(pairs)

def start():
	global snake
	global fruit

	getFruit(snake, fruit)
	move(snake.body, snake.route)

	if(not crashed(snake.body[0])):
		drawMap(snake, fruit)

		if (eatFruit(snake.body[0], fruit.pairs, fruit.count)):
			riseSnake(snake)
			fruit.count -= 1

		root.after(100, start)
	else:
		getResult()

	
def move(body, route):
	global STEP

	for i in reversed(range(1, len(body))):
		body[i].x1, body[i].y1 = body[i - 1].x1, body[i - 1].y1
		body[i].x2, body[i].y2 = body[i - 1].x2, body[i - 1].y2

	if (route == UP):
		body[0].y1 -= STEP
		body[0].y2 -= STEP

	if (route == LEFT):	
		body[0].x1 -= STEP
		body[0].x2 -= STEP

	if (route == RIGHT):	
		body[0].x1 += STEP
		body[0].x2 += STEP

	if (route == DOWN):	
		body[0].y1 += STEP
		body[0].y2 += STEP


def main(event):
	root.bind('<KeyPress-Up>', onUp)
	root.bind('<KeyPress-Down>', onDown)
	root.bind('<KeyPress-Left>', onLeft)
	root.bind('<KeyPress-Right>', onRight)

	pairs = Pairs()
	pairs.x1, pairs.y1 = X_START, Y_START
	pairs.x2, pairs.y2 = X_START + STEP, Y_START + STEP
	snake.body.append(pairs)

	start() 
	
btn.place(x = (SIZE_H - 100) / 2,  y = SIZE_H + 10, width = 100,  height = 40)
btn.bind("<Button-1>", main)

root.mainloop() 
