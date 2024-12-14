from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

gameover = False
pause = False
score = 0
lives = 3
miss = 0

shooter_x, shooter_y, shooter_r = 225, 20, 12

circle_speed = 0.3
circles_no = random.randint(1, 5)

class Circle:
    global circle_speed

    def __init__(self):
        self.x = random.randrange(20, 425, 5)
        self.y = 423
        self.r = random.randint(15, 30)
        self.speed = circle_speed
        
        


class Fire:
    global shooter_x, shooter_y, shooter_r, circle_speed

    def __init__(self):
        self.x = shooter_x
        self.y = shooter_y + (2 * shooter_r)
        self.r = shooter_r
        self.fired = False
        self.speed = circle_speed

circle_list = [Circle() for count in range(circles_no)]
fire_list = []
special_circle_list = []




#Draw functions 

def draw_point(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_shooter():
    glColor3f(1.0, 0.7, 0.0)  # Setting color for the rocket body
    # Rocket body
    mpl(shooter_x - 10, shooter_y, shooter_x + 10, shooter_y)  # Bottom line
    mpl(shooter_x - 10, shooter_y, shooter_x - 10, shooter_y + 40)  # Left side
    mpl(shooter_x + 10, shooter_y, shooter_x + 10, shooter_y + 40)  # Right side
    mpl(shooter_x - 10, shooter_y + 40, shooter_x + 10, shooter_y + 40)  # Top line

    # Rocket nose
    mpl(shooter_x - 10, shooter_y + 40, shooter_x, shooter_y + 55)  # Left diagonal
    mpl(shooter_x + 10, shooter_y + 40, shooter_x, shooter_y + 55)  # Right diagonal

    glColor3f(1.0, 0.4, 0.0)  # Set color for the fins
    # Left fin
    mpl(shooter_x - 10, shooter_y, shooter_x - 20, shooter_y )
    mpl(shooter_x - 20, shooter_y , shooter_x - 10, shooter_y + 10)

    # Right fin
    mpl(shooter_x + 10, shooter_y, shooter_x + 20, shooter_y )
    mpl(shooter_x + 20, shooter_y , shooter_x + 10, shooter_y + 10)

    glColor3f(1.0, 1.0, 0.0)  # Set color for the rocket thrusters
    # Thrusters
    mpl(shooter_x - 8, shooter_y, shooter_x - 8, shooter_y - 10)
    mpl(shooter_x, shooter_y, shooter_x, shooter_y - 10)
    mpl(shooter_x + 8, shooter_y, shooter_x + 8, shooter_y - 10)


def draw_circle():
    global circle_list, special_circle_list, gameover

    if gameover == False:
        for circles in circle_list:
            glColor3f(1,0.7,0)
            mcl(circles.x, circles.y, circles.r)
            
        for special in special_circle_list:
            glColor3f(*special.color)
            mcl(special.x, special.y, special.r)

class SpecialCircle(Circle):
    def __init__(self):
        super().__init__()
        self.color = (1, 0, 1)
        self.resizing_speed = 0.1
        self.resizing_direction = 1
        
    def update_size(self):
        self.r += self.resizing_direction * self.resizing_speed
        
        if self.r > 30 or self.r < 15:
            self.resizing_direction *= -1
            
            
def draw_fire():
    global fire_list, gameover

    if gameover == False:
        for fires in fire_list:
            fires.fired = True

            if fires.fired == True:
                draw_triangle(fires.x, fires.y, fires.r)
                
                
def draw_triangle(x, y, size):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x - size, y - size)
    glVertex2f(x + size, y - size)
    glEnd()
    
    
def circle_hit():
    global circle_list, special_circle_list, fire_list, score

    for circles in circle_list:
        for fires in fire_list:
            x0_dist = abs(circles.x - fires.x)
            y0_dist = abs(circles.y - fires.y)

            rad_dist = circles.r + fires.r

            center_dist = math.sqrt((x0_dist ** 2) + (y0_dist ** 2))

            if center_dist <= rad_dist:
                score += 1
                fires.fired = False
                circle_list.remove(circles)
                fire_list.remove(fires)
                print('Score:', score)
                
    for special in special_circle_list:
        for fires in fire_list:
            x0_dist = abs(special.x - fires.x)
            y0_dist = abs(special.y - fires.y)
            rad_dist = special.r + fires.r
            center_dist = math.sqrt((x0_dist ** 2) + (y0_dist ** 2))
            
            if center_dist <= rad_dist:
                score += 10
                fires.fired = False
                special_circle_list.remove(special)
                fire_list.remove(fires)
                print("Special Target hit! Score: ", score)

    glutPostRedisplay()


#Game functions
def game_overs():
    global circle_list, special_circle_list, shooter_x, shooter_y, shooter_r, gameover, lives, fire_list, miss

    for circles in circle_list:
        # CASE 1: Collusion check korbo
        if (circles.y - circles.r) <= (shooter_y + shooter_r):
            if (((circles.x - circles.r) <= (shooter_x + shooter_r)) and (
                    (circles.x + circles.r) >= (shooter_x - shooter_r))):
                gameover = True
                print('Game Over! Final Score:', score)
                
            if (circles.y + circles.r) <= 0:
                circle_list.remove(circles)
                miss += 1
                print(f"Missed a circle! Lives left: {lives}")
                
    # CASE 1: Eikhane Collusion check korbo for special circles             
    for special in special_circle_list:
        if (special.y - special.r) <= (shooter_y + shooter_r):
            if (((special.x - special.r) <= (shooter_x + shooter_r)) and ((special.x + special.r) >= (shooter_x - shooter_r))):
                gameover = True
                print('Game Over! Final Score:', score)
                return
            
        if (special.y + special.r) <= 0:
            special_circle_list.remove(special)
            miss += 1
            print(f"Missed a special circle! Lives Left: {lives}")

    # CASE 2: game over hoye jabe jodi total miss 3 hoy
    if lives <= 0:
        gameover = True
        print('Game Over! Final Score:', score)
        print('You have no lives left!')

    # # CASE 3
    # for fires in fire_list:
    #     if (fires.y + fires.r) >= 450:
    #         fire_list.remove(fires)
    #         miss += 1
    #         print('Misses:', miss)

    # if miss == 3:
    #     gameover = True
    #     print('Game Over! Final Score:', score)
    #     print('Misses:', miss)

    # glutPostRedisplay()




# MCL algo
def mcl(x0, y0, r):
    x, y = 0, r
    d = 1 - r

    draw_point(x + x0, y + y0)

    while x <= y:
        de = ((2 * x) + 3)
        dne = ((2 * x) - (2 * y) + 5)

        if d < 0:
            d += de
            x += 1
        else:
            d += dne
            x += 1
            y -= 1

        draw_point(x + x0, y + y0)
        draw_point(-x + x0, y + y0)
        draw_point(-x + x0, -y + y0)
        draw_point(x + x0, -y + y0)
        draw_point(y + x0, x + y0)
        draw_point(-y + x0, x + y0)
        draw_point(-y + x0, -x + y0)
        draw_point(y + x0, -x + y0)

# MPL algo
def mpl(x0, y0, x1, y1):
    zone = findzone(x0, y0, x1, y1)
    x0, y0 = converttozone0(zone, x0, y0)
    x1, y1 = converttozone0(zone, x1, y1)

    dx = x1 - x0
    dy = y1 - y0

    dne = 2 * dy - 2 * dx
    de = 2 * dy

    dinit = 2 * dy - dx

    while x0 <= x1:
        if dinit >= 0:
            dinit += dne
            x0 += 1
            y0 += 1
        else:
            dinit += de
            x0 += 1

        a, b = converttozoneM(zone, x0, y0)
        draw_point(a, b)



# Buttons in the game
def pause_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490)
    mpl(240, 450, 240, 490)

def play_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490)
    mpl(210, 450, 240, 469)
    mpl(210, 491, 240, 471)

def cancel_button():
    glColor3f(1.0, 0.0, 0.0)
    mpl(400, 450, 435, 490)
    mpl(400, 490, 435, 450)

def restart_button():
    glColor3f(0.0, 0.75, 0.8)
    mpl(15, 470, 50, 470)
    mpl(15, 470, 32.5, 490)
    mpl(15, 470, 32.5, 450)




# Zone Conversion parts       
def findzone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6

    return zone

def converttozone0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def converttozoneM(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y



# Keyboard button stuff          
keys = {b'a': False, b'd': False}

def keyboardListener(key, x, y):
    global keys, fire_list
    
    if not gameover and not pause:
        if key in keys:
            keys[key] = True
        elif key == b' ':
            fire_list.append(Fire())
            
    glutPostRedisplay()

def keyboardUpListener(key, x, y):
    global keys
    
    if key in keys:
        keys[key] = False
        
def mouseListener(button, state, x, y):
    global pause, score, gameover, lives, miss, shooter_x, shooter_y, shooter_r, circle_speed, circle_list, fire_list

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 210 <= x <= 240 and 10 <= y <= 50:
            if gameover == False:
                if pause == False:
                    pause = True
                    print('Paused')
                else:
                    pause = False
        elif 15 <= x <= 50 and 10 <= y <= 50:
            if gameover == True:
                gameover = False

            print('Starting Over')

            score = 0
            lives = 3
            miss = 0

            shooter_x, shooter_y, shooter_r = 225, 20, 12

            circle_speed = 0.3
            circles_no = random.randint(1, 5)

            circle_list = [Circle() for count in range(circles_no)]
            fire_list = []

        elif 400 <= x <= 435 and 10 <= y <= 50:
            gameover = True
            print('Goodbye! Final Score:', score)
            glutLeaveMainLoop()

    glutPostRedisplay()

def animate():
    global fire_list, shooter_x, special_circle_list
    
    if not gameover and not pause:
        #shooter er position update hocche continiously
        if keys[b'a'] and shooter_x > 16:
            shooter_x -= 0.85  #speed
            
        if keys[b'd'] and shooter_x < 434:
            shooter_x += 0.85
            
        for fires in fire_list:
            if (fires.y - fires.r) <= 450:
                fires.y += fires.speed
                
        for circles in circle_list:
            circles.y -= circles.speed
            
        for special in special_circle_list:
            special.y -= special.speed
            special.update_size()
            
        if random.random() < 0.002:
            special_circle_list.append(SpecialCircle())
            
        circle_hit()
        
        if not gameover:
            game_overs()


    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    animate()
    glColor3f(0.0, 0.0, 0.0)

    global fire_list, circle_list

    if pause == False:
        pause_button()
    else:
        play_button()

    cancel_button()
    restart_button()

    glColor3f(0.7, 0.6, 0.2)
    draw_shooter()

    if gameover == False:
        draw_fire()
        draw_circle()

    if circle_list == []:
        circle_list = [Circle() for count in range(circles_no)]

    draw_circle()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(450, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Circle Shooter Game")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutKeyboardUpFunc(keyboardUpListener)
glutMainLoop()