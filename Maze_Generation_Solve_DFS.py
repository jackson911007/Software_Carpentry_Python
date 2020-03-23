from PIL import Image
import time
import random
import numpy as np


def get_colors():
    '''
    Colors map that the maze will use:
        0 - Black - A wall
        1 - White - A space to travel in the maze
        2 - Green - A valid solution of the maze
        3 - Red - A backtracked position during maze solving
        4 - Blue - Start and Endpoints of the maze

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (0, 0, 255),
    }


def save_maze(maze, blockSize=10, name="maze"):
    '''
    This will save a maze object to a file.

    **Parameters**

        maze: *list, list, int*
            A list of lists, holding integers specifying the different aspects
            of the maze:
                0 - Black - A wall
                1 - White - A space to travel in the maze
                2 - Green - A valid solution of the maze
                3 - Red - A backtracked position during maze solving
                4 - Blue - Start and Endpoints of the maze
        blockSize: *int, optional*
            How many pixels each block is comprised of.
        name: *str, optional*
            The name of the maze.png file to save.

    **Returns**

        None
    '''
    nBlocks = len(maze)
    dims = nBlocks * blockSize  # transfer the pixel size to maze size
    colors = get_colors()  # get the color from get_color dict
    # Verify that all values in the maze are valid colors.
    ERR_MSG = "Error, invalid maze value found!"
    assert all([x in colors.keys() for row in maze for x in row]), ERR_MSG
    # Creates a new image with name, size, color
    img = Image.new("RGB", (dims, dims), color=0)
    # Parse "maze" into pixels
    for jx in range(nBlocks):
        for jy in range(nBlocks):
            x = jx * blockSize
            y = jy * blockSize  # Set up new coordination for maze
            for i in range(blockSize):
                for j in range(blockSize):
                    img.putpixel((x + i, y + j), colors[maze[jx][jy]])
                    # maze[jx][jy] is a given block in maze (matrix), which
                    # will have a corresponding value. We set its value to be
                    # the keys in colors dictionary and call RGB values from
                    # colors{} by colors[keys]
    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)


def load_maze(filename, blockSize=10):
    '''
    This will read a maze from a png file into a 2d list with values
    corresponding to the known color dictionary.

    **Parameters**

        filename: *str*
            The name of the maze.png file to load.
        blockSize: *int, optional*
            How many pixels each block is comprised of.

    **Returns**

        maze: *list, list, int*
            A 2D array holding integers specifying each block's color.
    '''
    if ".png" in filename:
        filename = filename.split(".png")[0]
    img = Image.open(filename + ".png")
    dims, _ = img.size
    nBlocks = int(dims / blockSize)
    colors = get_colors()
    # reciprocal of dictionary key: value
    color_map = {v: k for k, v in colors.items()}
    maze = [[0 for x in range(nBlocks)] for y in range(nBlocks)]
    # Parse pixels into the maze array
    for i, x in enumerate(range(0, dims, dims // nBlocks)):
        for j, y in enumerate(range(0, dims, dims // nBlocks)):
            px = x
            py = y
            maze[i][j] = color_map[img.getpixel((px, py))]

    # enumerate(list) counts the value from range
    # 0-dims with an interval dims//nBlocks)
    # Start from 0.
    return maze


def pos_chk(x, y, nBlocks):
    '''
    Validate if the coordinates specified (x and y) are within the maze.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        nBlocks: *int*
            How many blocks wide the maze is.  Should be equivalent to
            the length of the maze (ie. len(maze)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    return x >= 0 and x < nBlocks and y >= 0 and y < nBlocks


def generate_maze(nBlocks, name="maze", start=(0, 0), blockSize=10,
                  slow=False):
    '''
    Generate a maze using the Depth First Search method.

    **Parameters**

        nBlocks: *int*
            The number of blocks in the maze (x and y dims are the same).
        name: *str, optional*
            The name of the output maze.png file.
        start: *tuple, int, optional*
            Where the maze will start from, and the initial direction.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''
    # Create a while true loop to
    # 1. Search for Possible route
    # 2. Take movements
    while True:

        # Create the maze by using numpy method
        maze = np.zeros((nBlocks, nBlocks), dtype=np.uint8)
        # Set up a stack list, which is the route of our maze
        stack = [start]
        # Set up the starting point
        # Label the strating point with color white
        y, x = stack[-1]
        maze[y][x] = 1
        while len(stack) > 0:
            # Set up a check list and put the boundary conditions
            # check = [L, R, U, D] for directions
            check = []
            # check the position using giving function
            # There are 4 boaders, which we need to check
            # 1. The left hand side. If maze moves to left
            #   a. When y = 0, it will ignore the up-left block
            #   b. When x = 1, it will ignore the left-left block
            #   c. When y = the lower boarder, it will ignore the
            #      down-left block
            # Each of these coniditons are a pair of confitions so use:
            # (if, elif)
            # I used count to collect the coniditons. if three conditions from
            # the three pairs are matches. the condition will be put in the
            # check list.
            if pos_chk(x, y, nBlocks):
                if x > 0 and maze[y][x - 1] == 0:
                    count = 0
                    if y == 0:
                        count += 1
                    elif maze[y - 1][x - 1] == 0:
                        count += 1
                    if x == 1:
                        count += 1
                    elif maze[y][x - 2] == 0:
                        count += 1
                    if y == nBlocks - 1:
                        count += 1
                    elif maze[y + 1][x - 1] == 0:
                        count += 1
                    if count == 3:
                        check.append('L')
            # 2. The Upper side. If maze moves up
            #   a. When x = 0, it will ignore the left-up block
            #   b. When y = 1, it will ignore the up-up block
            #   c. When x = the lower boarder, it will ignore the
            #      right-up block
            # Each of these coniditons are a pair of confitions so use:
            # (if, elif)
            # I used count to collect the coniditons. if three conditions from
            # the three pairs are matches. the condition will be put in the
            # check list.
                if y > 0 and maze[y - 1][x] == 0:
                    count = 0
                    if x == 0:
                        count += 1
                    elif maze[y - 1][x - 1] == 0:
                        count += 1
                    if y == 1:
                        count += 1
                    elif maze[y - 2][x] == 0:
                        count += 1
                    if x == nBlocks - 1:
                        count += 1
                    elif maze[y - 1][x + 1] == 0:
                        count += 1
                    if count == 3:
                        check.append('U')
            # 3. The Right side. If maze moves to right
            # Same concept with the previous case
            # Each of these coniditons are a pair of confitions so use:
            # (if, elif)
            # I used count to collect the coniditons. if three conditions from
            # the three pairs are matches. the condition will be put in the
            # check list.
                if x < nBlocks - 1 and maze[y][x + 1] == 0:
                    count = 0
                    if x == nBlocks - 2:
                        count += 1
                    elif maze[y][x + 2] == 0:
                        count += 1
                    if y == nBlocks - 1:
                        count += 1
                    elif maze[y + 1][x + 1] == 0:
                        count += 1
                    if y == 0:
                        count += 1
                    elif maze[y - 1][x + 1] == 0:
                        count += 1
                    if count == 3:
                        check.append('R')
            # 3. The down side. If maze move down
            # Same concept with the previous case
            # Each of these coniditons are a pair of confitions so use:
            # (if, elif)
            # I used count to collect the coniditons. if three conditions from
            # the three pairs are matches. the condition will be put in the
            # check list.
                if y < nBlocks - 1 and maze[y + 1][x] == 0:
                    count = 0
                    if x == 0:
                        count += 1
                    elif maze[y + 1][x - 1] == 0:
                        count += 1
                    if y == nBlocks - 2:
                        count += 1
                    elif maze[y + 2][x] == 0:
                        count += 1
                    if x == nBlocks - 1:
                        count += 1
                    elif maze[y + 1][x + 1] == 0:
                        count += 1
                    if count == 3:
                        check.append('D')

            # check the check list if there is any possible direction to move
            if len(check) > 0:
                # randomize the movement in the check list
                Direction = random.choice(check)
                # determine how the the point move in different direction
                if Direction == 'L':
                    x -= 1
                    maze[y][x] = 1
                    stack.append((y, x))
                if Direction == 'U':
                    y -= 1
                    maze[y][x] = 1
                    stack.append((y, x))
                if Direction == 'R':
                    x += 1
                    maze[y][x] = 1
                    stack.append((y, x))
                if Direction == 'D':
                    y += 1
                    maze[y][x] = 1
                    stack.append((y, x))
            else:
                # if there is no possible direction to move, remove
                # the last point and trace back to the previous point
                # put the coordination number to x, y
                stack.pop()
                if len(stack) > 0:
                    y, x = stack[-1]

            # If slow, we can generate and solve step by step
            if slow:
                maze[start[0]][start[1]] = 4
                maze[nBlocks - 1][nBlocks - 1] = 4
                save_maze(maze, blockSize=blockSize, name=name)
                time.sleep(0.2)
                maze[start[0]][start[1]] = 1
                maze[nBlocks - 1][nBlocks - 1] = 1

        # When the start point is the end point, break the loop
        if maze[nBlocks - 1][nBlocks - 1] == 1:
            break
    # I found a error that take place in my the code.
    # Sometime there is no valid path to the end but it still generate the
    # maze. Here, I add a condition, only if there is a pssible path
    # in the next to the end, can we generate the maze
    if maze[nBlocks - 2][nBlocks - 1] == 0 and maze[nBlocks - 1][nBlocks - 2] == 0:
        generate_maze(nBlocks, name, start, blockSize, slow)
    else:
        maze[start[0]][start[1]] = 4
        maze[nBlocks - 1][nBlocks - 1] = 4
        save_maze(maze, blockSize=blockSize, name=name)

    # Information:
    # 1. https://blog.csdn.net/juzihongle1/article/details/73135920fbclid=
    # IwAR0tfyz13yyEaAWbJ2zaB39dOEFQfL8AFYRNGv2ozUPTETQyasJy15mZ76Q


def solve_maze(filename, start=(0, 0), end=(49, 49), blockSize=10, slow=False):
    '''
    Solve a maze using the Depth First Search method.

    **Parameters**

        filename: *str*
            The name of the maze.png file to be solved.
        start: *tuple, int, optional*
            Where the maze will start from.
        end: *tuple, int, optional*
            Where the maze will end.
        blockSize: *int, optional*
            How many pixels each block will be.
        slow: *bool, optional*
            Whether to save and lag on generation so as to view the mazegen.

    **Returns**

        None
    '''
    # laod the maze and set up the first point
    maze = load_maze(filename, blockSize)
    nBlocks = len(maze)
    stack = [start]
    y, x = stack[-1]
    # set up the keypoint from start point to end point
    maze[y][x] = 4
    maze[end[0]][end[1]] = 1

    # Similar to the previous code, but simpler. We do not have to condisder
    # the border condition. Here, we only need to follow the path we create
    # from generate maze
    while len(stack) > 0:
        # Put the possible routes to the check list, and follow the path
        # we create for different direction
        # check = [L, R, U, D] for directions
        check = []
        if pos_chk(x, y, nBlocks):
            if x > 0 and maze[y][x - 1] == 1:
                check.append('L')
            if y > 0 and maze[y - 1][x] == 1:
                check.append('U')
            if x < nBlocks - 1 and maze[y][x + 1] == 1:
                check.append('R')
            if y < nBlocks - 1 and maze[y + 1][x] == 1:
                check.append('D')

            # See if there is any correct path to mave in the check list
            if len(check):
                # randomize the movement in the check list
                move_direction = random.choice(check)
                if move_direction == 'L':
                    x -= 1
                    maze[y][x] = 2
                    stack.append((y, x))
                if move_direction == 'U':
                    y -= 1
                    maze[y][x] = 2
                    stack.append((y, x))
                if move_direction == 'R':
                    x += 1
                    maze[y][x] = 2
                    stack.append((y, x))
                if move_direction == 'D':
                    y += 1
                    maze[y][x] = 2
                    stack.append((y, x))
            else:
                # if there is no possible direction to move, remove
                # the last point and trace back to the previous point
                # put the coordination number to x, y
                stack.pop()
                # change the color of the invalid path in this process
                maze[y][x] = 3
                if len(stack) > 0:
                    y, x = stack[-1]
            if slow:
                maze[start[0]][start[1]] = 4
                maze[end[0]][end[1]] = 4
                save_maze(maze, blockSize=blockSize, name="Solution")
                time.sleep(0.5)
                maze[start[0]][start[1]] = 2
                maze[end[0]][end[1]] = 1

        if y == end[0] and x == end[1]:
            break

    maze[start[0]][start[1]] = 4
    maze[end[0]][end[1]] = 4
    save_maze(maze, blockSize=blockSize, name="Solution")


if __name__ == "__main__":
    generate_maze(50, name="maze", start=(0, 0), blockSize=10, slow=False)
    solve_maze("maze", start=(0, 0), end=(49, 49), blockSize=10, slow=False)
