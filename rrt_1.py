import math, sys, pygame, random
from math import *
from pygame import *

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

# Set global variables
XDIM = 720
YDIM = 500
WINDOW_SIZE = [XDIM, YDIM]
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
EPSILON = 7.0
NUMNODES = 5000
GAME_LEVEL = 1

pygame.init()
fps_clock = pygame.time.Clock()

# Set visual parameters 
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('RRT: Set Starting Point, then Goal Point')
white = 255, 255, 255
black = 20, 20, 40
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0, 255, 255

# RRT variables
count = 0
rect_obs = []

# Compute distance between two points
def dist(p1, p2):
    return sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]-p2[1]) * (p1[1]-p2[1]))

# Check for collision of circular configuration
def point_circle_collision(p1, p2, radius):
    distance = dist(p1, p2)
    if(distance <= radius):
        return True
    return False

# Check if points abide by step size constraint
def step_from_to(p1, p2):
    if dist(p1, p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1], p2[0]-p1[0])
        return p1[0] + EPSILON * cos(theta), p1[1] + EPSILON * sin(theta)
    
# Check if the newly generated point collides with an obstacle 
def collides(p):
    for rect in rect_obs:
        if rect.collidepoint(p) == True:
            return True
    return False
    
# Generate new random point that doesn't collide with an obstacle
def get_random_clear():
    while True:
        p = random.random() * XDIM, random.random() * YDIM
        no_collision = collides(p)
        if no_collision == False:
            return p

# Initialize obstacles in window
def init_obstacles(config_num):
    global rect_obs
    rect_obs = []
    print("config" + str(config_num))

    if(config_num == 0):
        rect_obs.append(pygame.Rect((XDIM/2.0-50, YDIM/2.0-100), (100, 200)))
    if(config_num == 1):
        rect_obs.append(pygame.Rect((40, 10), (100, 200)))
        rect_obs.append(pygame.Rect((500, 200), (500, 200)))
    if(config_num == 2):
        rect_obs.append(pygame.Rect((40, 10), (100, 200)))
    if(config_num == 3):
        rect_obs.append(pygame.Rect((40, 10), (100, 200)))

    for rect in rect_obs:
        pygame.draw.rect(screen, red, rect)

        
def reset():
    global count
    screen.fill(black)
    init_obstacles(GAME_LEVEL)
    count = 0

    
def main():
    global count

    init_pose_set = False
    init_point = Node(None, None)
    goal_pose_set = False
    goal_point = Node(None, None)
    current_state = 'init'

    nodes = []
    reset()    

    while True:
        if current_state == 'init':
            print('goal point not yet set')
            fps_clock.tick(10)
       
        elif current_state == 'goal_found':
            # traceback 
            current_node = goal_node.parent
            #pygame.display.set_caption('Goal Reached')
            #print('Goal Reached')

            while current_node.parent != None:
                pygame.draw.line(screen, cyan, current_node.point, \
                                 current_node.parent.point)
                current_node = current_node.parent
                optimize_phase = True
                
        elif current_state == 'optimize':
            fps_clock.tick(0.5)
            pass
        
        elif current_state == 'build_tree':
            count = count+1
            pygame.display.set_caption("Performing RRT")
            if count < NUMNODES:
                found_next = False
                while found_next == False:
                    rand = get_random_clear()
                    parent_node = nodes[0]

                    # Identify the nearest vertex
                    for p in nodes:
                        if dist(p.point, rand) <= dist(parent_node.point, rand):
                            new_point = step_from_to(p.point, rand)
                            if collides(new_point) == False:
                                parent_node = p
                                found_next = True

                new_node = step_from_to(parent_node.point, rand)
                nodes.append(Node(new_node, parent_node))
                pygame.draw.line(screen, white, parent_node.point, new_node)

                if point_circle_collision(new_node, goal_point.point, GOAL_RADIUS):
                    current_state = 'goal_found'
                    goal_node = nodes[len(nodes) - 1]

                if count % 100 == 0:
                    print("node: " + str(count))
                    
            else:
                print("Ran out of nodes... :( ")
                return;

        # Handle events
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if current_state == 'init':
                    if init_pose_set == False:
                        nodes = []
                        if collides(e.pos) == False:
                            print('initial point set: ' + str(e.pos))

                            init_point = Node(e.pos, None)
                            # start in center
                            nodes.append(init_point)
                            init_pose_set = True
                            pygame.draw.circle(screen, blue, \
                                               init_point.point, \
                                               GOAL_RADIUS)
                    elif goal_pose_set == False:
                        print('goal point set: ' + str(e.pos))
                        if collides(e.pos) == False:
                            goal_point = Node(e.pos, None)
                            goal_pose_set = True
                            pygame.draw.circle(screen, green, \
                                               goal_point.point, \
                                               GOAL_RADIUS)
                            current_state = 'build_tree'
                else:
                    current_state = 'init'
                    init_pose_set = False
                    goal_pose_set = False
                    reset()

        pygame.display.update()
        fps_clock.tick(10000)
            

if __name__ == '__main__':
    main()
input("press Enter to quit")
