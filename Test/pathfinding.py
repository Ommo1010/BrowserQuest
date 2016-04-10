grid = [[0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 2]]

def search(x, y, grid):
    if grid[x][y] == 2:
        print("found",x,y)
        return(x*30,y*30)

    elif grid[x][y] == 1:
        print("wall",x,y)
        return False
    elif grid[x][y] == 3:
        print("visited",x,y)
        return False
    print("visiting",x,y)
    # mark as visited
    grid[x][y] = 3
    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid)-1 and search(x+1, y, grid))
        or (y > 0 and search(x, y-1, grid))
        or (x > 0 and search(x-1, y, grid))
        or (y < len(grid)-1 and search(x, y+1, grid))):
        return True
    return False
search(0, 0, grid)
