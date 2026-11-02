import matplotlib.pyplot as plt
import numpy as np
import random

CELL_SIZE = 10

#Direction order: down, right, up, left

DIRECTIONS = [(1,0),(0,1),(-1,0),(0,-1) ]

#Load and process maze

def load_maze(filename):
    maze = plt.imread(filename)
    #Convert image to grayscale
    if maze.ndim == 3:
        gray = np.mean(maze[:, :, :3], axis=2)
    else:
        gray = maze
    #Sample the centre of each 10x10 square
    #This converts the 210x210 image into a 21x21 grid
    gray_grid = gray[5::CELL_SIZE, 5::CELL_SIZE]

    #White = walkable, black = wall
    walkable = gray_grid > 0.5

    return maze, walkable


#Display maze in terminal

def display_maze(walkable):
    print("\nMaze representation:")
    print("S = Start | E = Exit | . = Corridor | # = Wall\n")
    start, end = find_endpoints(walkable)

    for y in range(walkable.shape[0]):
        row = ""

        for x in range (walkable.shape[1]):
            if (y,x) == start:
                row += "S "
            elif (y,x) == end:
                row += "E "
            elif walkable[y,x]:
                row += ". "
            else: 
                row += "# "
        print(row)

#Find start and end points
def find_endpoints(walkable):
    h,w = walkable.shape
    openings = []
    #Check top and bottom borders
    for x in range(w):
        if walkable[0,x]:
            openings.append((0, x))
        if walkable[h - 1, x]:
            openings.append((h - 1, x))
        
    #check left and right and borders
    for y in range(1, h - 1):
        if walkable[y, 0]:
            openings.append((y, 0))
        if walkable[y, w - 1]:
            openings.append((y, w - 1))
    openings = list(dict.fromkeys(openings))

    if len(openings) != 2:
        raise ValueError(f"Expected 2 maze openings, found {len(openings)}."
        "Check the maze image or set start and end manually")
    return openings[0], openings[1]


#Backtracking Algorithm

def backtracking(walkable, start, end):
    h,w = walkable.shape
    visited = np.zeros((h,w), dtype=bool)
    #Stack represents the current path
    stack = [start]
    visited[start] = True
    while stack:
        y,x = stack[-1]
        #check whether the exit has been reached
        if (y,x) == end:
            return stack.copy(), visited
        moved = False

        #explore directions in the specified order
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx

            if ( 0<= ny < h and 0 <= nx < w and walkable[ny, nx] and not visited[ny, nx]):
                visited[ny, nx] = True
                stack.append((ny, nx))
                moved = True

                break
        #if no available directions exists, backtrack
        if not moved:
            stack.pop()
        
        #No solution found
        return None, visited


#Las Vegas Algorithm

#step limit of 200.
def las_vegas(walkable, start, end, max_steps=200):
    h,w = walkable.shape
    visited = np.zeros((h,w), dtype=bool)
    y,x = start
    path = [start]
    visited[y,x] = True
    moves = 0

    while moves < max_steps:
        #check whether the exit has been reached
        if (y,x) == end:
            return path, visited, moves
        choices = []

        #find all walkable neighbouring positions
        for dy, dx in DIRECTIONS:
            ny = y + dy
            nx = x + dx

            if ( 0<= ny < h and 0 <= nx < w and walkable[ny, nx]):
                choices.append((ny, nx))
        #no possible movements found
        if not choices:
            break
        #Randomly select the next position
        y,x = random.choice(choices)

        visited[y,x] = True
        path.append((y,x))

        moves += 1
    # check the exit after the final move
    if (y,x) == end:
        return path, visited, moves

    return None, visited, moves
                

#visualise all visited places

def save_visualisation(original, visited, path, start, end, filename):
    if original.ndim == 2:
        result = np.stack([original] * 3, axis= -1)
    else:
        result = original[:, :, :3].copy()
    #colour all visited squares red
    for y,x in zip(*np.where(visited)):
        y1 = y * CELL_SIZE
        x1 = x * CELL_SIZE

        result[y1:y1 + CELL_SIZE, x1:x1 + CELL_SIZE] = [1, 0, 0]
    #colour the successful solution path yellow

    if path is not None:
        for y, x in path:
            y1 = y * CELL_SIZE
            x1 = x * CELL_SIZE

            result[y1:y1 + CELL_SIZE, x1:x1 + CELL_SIZE] = [1, 0, 0]

    #mark entrance green
    sy, sx = start
    result[sy * CELL_SIZE:(sy + 1) * CELL_SIZE, sx * CELL_SIZE:(sx + 1) * CELL_SIZE,] = [0, 1, 0]

    #mark exit blue
    ey, ex = start
    result[ey * CELL_SIZE:(ey + 1) * CELL_SIZE, ex * CELL_SIZE:(ex + 1) * CELL_SIZE,] = [0, 0, 1]

    #Display result
    plt.figure(figsize=(9,9))
    plt.imshow(result)
    plt.title("Maze Exploration - Visitied places")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight")
    plt.show()
    
    print("\n Visualisation saved as:", filename)


def main():
        #load maze
        maze, walkable = load_maze("maze.png")
        print("Maze loaded successfully")
        print("Maze dimensions:", walkable.shape)

        #find entrance and exit
        start, end = find_endpoints(walkable)
        print("Start position:", start)
        print("Exit position:", end)

        #display maze in terminal
        display_maze(walkable)

        #Ask user to select an algorithm
        print("\nChoose a maze-solving algorithm:")
        print("1. Las Vegas")
        print("2. Backtracking")
        choice = input("\nEnter 1 or 2 ").strip()
        path = None

        #Run selected algorithm

        if choice == "1":
            print ("\n Running Las Vegas algorithm...")
            path, visited, moves = las_vegas(walkable, start, end, max_steps=200)
            print("Number of moves:", moves)
            filename = "maze_las_vegas.png"
        elif choice == "2":
            print("\nRunning Backtracking algorithm...")
            path, visited, moves = backtracking(walkable, start, end)
            filename = "maze_backtracking.png"
        else:
            print("Invalid choice. Please enter 1 or 2")

            return
        #display results

        if path is not None:
            print("\nSUCCESS! Exit found")
            print("Solution path length:", len(path))
        else:
            print("\nUNSUCCESSFUL! Exit not found")

        print("Total unique positions visited:", np.count_nonzero(visited))

        #visualise all visited places regardless of success

        save_visualisation(maze, visited, path, start, end, filename)

if __name__ == "__main__":
    main()



        


