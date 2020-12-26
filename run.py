"""
CISC204 - Course Modelling Project
Group 42
Minesweeper solver
December 6th, 2020

@author Graham Carkner (18gtc),
        Elliot Arbuthnot (18era3),
        Truman Be (18tb18),
        Reid Moffat (18rem8)
"""

# Imports below:
# The encoding is used to solve our model 
# Var is an object used to store our coolean conditions
# iff is used to determine the middle square's state
from lib204 import Encoding
from nnf import Var
from nnf.operators import iff

'''
Below are some initial 5x5 states we use for testing our code

INITIAL STATE VARIABLE EXPLANATION
-1: unknown spot / undiscovered mystery wowowow
-2: mine (in a real game, this would be a flag)
0 <= n <= 8: uncovered spot with n adjacent bombs (includes diagonals)
'''

# State 1 is a mine
state_1 = [
  [1, -1, -1, -1, -1],
  [1, -1, -1, -1,  2],
  [2, -2, -1,  3,  2],
  [3, -2,  5, -2,  1],
  [3, -2,  3,  1,  1]
]

# State 2 is a mine
state_2 = [
  [2,  1,  1,  2, -2],
  [1,  2, -1, -1, -1],
  [1,  3, -1,  1, -1],
  [1, -2, -1, -1,  3],
  [1,  1,  2,  2, -1]
]

# State 3 is safe
state_3 = [
  [-1, -1, -1, -1, -1],
  [-1, -1,  1,  0, -1],
  [-1,  1, -1,  1, -1],
  [-1,  0,  1, -2, -1],
  [-1, -1, -1, -1, -1]
]

# State 4 is a mine
state_4 = [
  [ 1,  1,  1,  0,  0],
  [ 1, -2,  2,  1,  0],
  [ 2,  3, -1,  1,  0],
  [ 2, -2,  3,  2,  1],
  [-1, -1, -1, -1, -1]
]

# State 5 is a mine
state_5 = [
  [ 1,  1,  1, 0, 0],
  [ 1, -2,  2, 1, 0],
  [ 2, -1, -1, 1, 0],
  [-1, -1, -1, 1, 0],
  [ 0,  0,  0, 0, 0]
]

# State 6 is unknown
state_6 = [
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1]
]

# State 7 is safe
state_7 = [
  [0,  0,  0,  0, 0],
  [0, -1, -2,  1, 0],
  [0, -1, -1, -1, 0],
  [0, -1, -1, -1, 0],
  [0,  0,  0,  0, 0]
]

# State 8 is unknown
state_8 = [
  [-1, -1,  1, -1, -1],
  [-1,  2, -2,  2, -1],
  [-1, -1, -1, -1, -1],
  [-1,  2, -1, -1, -1],
  [-1, -1, -1, -1, -1]
]

# State 9 is unknown
state_9 = [
  [1,  2, -1, -1,  2],
  [1, -2,  3,  3, -2],
  [1,  2, -1,  2,  1],
  [1,  3, -1,  3,  1],
  [1, -2, -2, -2,  1]
]

# Keeps all the states together for ease of access
states = [state_1, state_2, state_3, state_4, state_5, state_6, state_7,
          state_8, state_9]
expected = ["mine", "mine", "safe", "mine", "mine", "unknown", "safe",
            'unknown', 'unknown']

'''
Boolean condition guide:

Each of the following lists contain the boolean values for a specified condition
for each square on the 5x5 board. Each square is either True or False for each
condition

-x is a revealed spot where the number of adjacent mines is equal to the number
of adjacent squares that we know are mines (x is 'satisfied'. This means that
all of the adjacent unknown squares are safe)
    -This condition is used to check if the middle square is safe. We can only be
    sure of the safety of the middle square if there is at least one adjacent x
-y is a revealed spot where the number of adjacent mines is equal to the number
of adjacent known mines and the number of adjacent unrevealed squares (this
means that every unknown square around a y square is a mine)
    -This condition is used to check if the middle square is a mine. We can only
    be sure the middle square is a mine if there is at least one adjacent y
-m (mine) is a square that has not been revealed and we know it has a mine (a
flag in a real game of minesweeper)
-s (safe) is a square that has not been revealed and we know it does not have a
mine (a square that you would click to reveal in a real game of minesweeper)
-u (unknown) is a square that has not been revealed and we don't know if it is a
mine or a safe spot

Notes:
-If a square is revealed, it can have 3 possible states:
    1. True x condition and False for every other condition
    2. True y condition and False for every other condition
    3. False for all conditions (the square is revealed but we aren't sure where
    all the adjacent mines are, i.e not an x or a y. For example, a square with
    2 adjacent mines but we only know where one of them is)

    Important: It is not possible in our case to have a True x condition and a
    True y condition. This would occur if a square is a satisfied x with no
    adjacent unknown squares; but this won't happen because the middle square is
    unknown and we only find x and y conditions for the inner 8 squares

-If a square is not revealed, it has to be one of the three revelaed conditions:
    1. If we know the square is a mine, m is True and all other conditions are False
    2. If we know the square is safe, s is True and all other conditions are False
    3. If we don't know if the square is a mine or safe, u is True and all other
    conditions are False
'''


# The x boolean condition for each square
x = [[], # row 1 
    [],  # row 2 
    [],  # row 3
    [],  # row 4
    []]  # row 5

# The y boolean condition for each square
y = [[], # row 1 
    [],  # row 2 
    [],  # row 3
    [],  # row 4
    []]  # row 5

# The m boolean condition for each square
m = [[], # row 1 
    [],  # row 2 
    [],  # row 3
    [],  # row 4
    []]  # row 5

# The u boolean condition for each square
u = [[], # row 1
    [],  # row 2
    [],  # row 3
    [],  # row 4
    []]  # row 5

# The s boolean condition for each square
s = [[], # row 1
    [],  # row 2
    [],  # row 3
    [],  # row 4
    []]  # row 5

# Encoding initialization
E = Encoding()


def set_initial_state(grid_setup):
    """
    Sets the inital state of a grid

    @param grid_setup: a 5x5 2-dimensional list of a grid state
    """
    grid_range = range(5) # A range variable used to iterate through the grid

    # Instantiates Var objects for u, m and s cases for the 5x5 grid
    for i in grid_range:
        for j in grid_range:
            # These create objects for each condition and state in the form
            # mij, uij and sij. For example, m12 would be the condition that
            # the square at coordinates (1, 2) is a bomb (coords start at (0, 0))
            m[i].append(Var('m' + str(i) + str(j)))
            u[i].append(Var('u' + str(i) + str(j)))
            s[i].append(Var('s' + str(i) + str(j)))

            # Each square's state is checked and constraints are added
            # The if conditional is used to ignore the center square since
            # we don't need constrainsts for it
            if not (i == 2 and j == 2):
                state = grid_setup[i][j]
                # Raises an exception if a square has an illegal value
                if not (-2 <= state <= 8):
                    raise Exception('error: each square of the grid must have a'
                                    ' value between -2 and 8 inclusive. Square '
                                    '[%d][%d] has a value of %d' %(i, j, state))

                if state == -2: # mine
                    E.add_constraint(m[i][j])
                else:
                    E.add_constraint(~m[i][j])

                if state == -1: # unknown
                    E.add_constraint(u[i][j])
                else:
                    E.add_constraint(~u[i][j])

                if state > -1: # revealed square
                    E.add_constraint(s[i][j])
                else:
                    E.add_constraint(~s[i][j])

    # Initializing x and y cases
    for i in grid_range:
        for j in grid_range:
            # We are only initializing the x and y truth values for the inner
            # 9 squares
            # The outer ring of squares can sometimes be determined for x and
            # y values, but that is beyond our scope
            if 0 < i < 4 and 0 < j < 4:
                set_X_truth(grid_setup, i, j)
                set_Y_truth(grid_setup, i, j)
            else:
                x[i].append(Var("x" + str(i) + str(j)))
                y[i].append(Var("y" + str(i) + str(j)))


def set_X_truth(grid_setup, i, j):
    """
    Sets the x truth values a given square in a grid

    @param grid_setup: 5x5 2-dimensional list of a grid state
           i: row number of the square
           j: column number of the square
    """

    # This constant list is used to quickly get the coordinates of adjacent squares
    coords = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
              [  i  , j - 1],             [  i  , j + 1],
              [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
    counter = 0 # Used for counting the number of adjacent mines

    for n in range(len(coords)):
        adjacent_row = coords[n][0]
        adjacent_col = coords[n][1]
        # The following conditional checks if the nth adjacent square is a mine
        if grid_setup[adjacent_row][adjacent_col] == -2:
            counter += 1
    
    # Instantiates a Var object for the x condition at the given coordinate and
    # sets a constraint for it
    x[i].append(Var("x" + str(i) + str(j)))
    if grid_setup[i][j] == counter:
        E.add_constraint(x[i][j])
    else:
        E.add_constraint(~x[i][j])


def set_Y_truth(grid_setup, i, j):
    """
    Sets the y truth values a given square in a grid

    @param grid_setup: 5x5 2-dimensional list of a grid state
           i: row number of the square
           j: column number of the square
    """

    # This constant list is used to quickly get the coordinates of adjacent squares
    coords = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
              [  i  , j - 1],             [  i  , j + 1],
              [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
    counter = 0 # Used for counting the number of adjacent mines or unknown squares

    for n in range(len(coords)):
        adjacent_square = grid_setup[coords[n][0]][coords[n][1]]
        # The following conditional checks if the nth adjacent square is a mine
        # or unknown
        if adjacent_square == -1 or adjacent_square == -2:
            counter += 1
    
    # Instantiates the y condition at the given coordinate and sets a constraint
    # for it
    y[i].append(Var("y" + str(i) + str(j)))
    if grid_setup[i][j] == counter:
        E.add_constraint(y[i][j])
    else:
        E.add_constraint(~y[i][j])


def set_truth_encodings():
    """
    Sets the constraints required to determine the state of the middle square
    """

    # If there are any adjacent squares with a True y condition, the middle square
    # is a mine. See the boolean condition guide (top) for an explanation
    E.add_constraint(iff((y[1][1] | y[1][2] | y[1][3] | y[2][1] | y[2][3]
                          | y[3][1] | y[3][2] | y[3][3]), m[2][2]))
    # If there are any adjacent squares with a True x condition, the middle square
    # is safe. See the boolean condition guide (top) for an explanation
    E.add_constraint(iff((x[1][1] | x[1][2] | x[1][3] | x[2][1] | x[2][3]
                          | x[3][1]| x[3][2] | x[3][3]), s[2][2]))
    # If the middle square isn't a mine or safe, it is unknown
    E.add_constraint(iff(~m[2][2] & ~s[2][2], u[2][2]))


def create_encoding(grid):
    """
    Calls all the functions in the correct order

    @param grid: 5x5 2-dimensional list minesweeper grid
    """
    set_initial_state(grid)
    set_truth_encodings()


def print_state(state, num):
    """
    Prints the minesweeper state similar to how it would look in a real game

    Prints a 'box' with each square being a number (of adjacent mines), a
    question mark (unknown) or an M (mine). Also includes the state number

    @param state: a 5x5 minesweeper grid
           num: the state 'number' (either a pre-define state or 'new')
    """
    grid_range = range(5) # A range variable used to iterate through the grid

    print("\nSTATE %s:"  %(str(num)))
    print("-----------")
    for i in grid_range:
        print('|', end='')
        for j in grid_range:
            square = state[i][j]
            if square == -2:
                print('M', end='')
            elif square == -1:
                print('?', end='')
            else:
                print(str(square), end='')
            if j < len(state[i]) - 1:
                print(" ", end='')
        print('|')
    print("-----------\n")


def make_mine_state():
    """
    Creates a new minesweeper state with user input
    """

    # Initializes a default state of all unknowns
    # This makes it easier to print out intermediary states
    new_state = [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ]

    # Prints out some instructions for how to properly input states
    print("\n=====CUSTOM STATE CREATION=====")
    print("Enter states row by row, Each square seperated by a space.")
    print("Ex. input: -1 -1 2 1 -2")
    print("Center spot should be unknown (-1), this is what it is solving for.")
    print("Key:")
    print("-2: mine")
    print("-1: unknown")
    print("0 <= n <= 8: revealed number square with n adjacent mines")

    # Applies user inputted numbers to the state
    for i in range(5):
        # Print out intermediate state
        print_state(new_state, "new")

        # Promts the user to input a row, checks if it is valid and applies 
        # it to the state if it is. If not, loop until a valid row is inputted
        while True:
            spot = input("Enter row %d: " %(i + 1))
            try:
                new_state[i]=[int(x) for x in spot.split()]
                if len(new_state[i]) == 5:
                    valid_row = True
                    for x in new_state[i]:
                        if not (-2 <= x <= 8):
                            print("Each value must be in the range [-2, 8]\n")
                            valid_row = False
                    if valid_row:
                        break
                else:
                    print("5 values required, try again.\n")
            except:
                print("Invalid row, try again.\n")
        if i == 2:
            # The middle square is always unknown since the algorithm needs
            # to solve for it. Putting in another value to the middle won't
            # break the encoding, but it is confusing
            new_state[2][2] = -1

    # Prints out the final state
    print_state(new_state, "new")

    # If the user creates their own state, it is added to the list of states
    # (for the duration of the program) and prompty tested
    states.append(new_state)
    test_state(len(states))


def test_state(state_num):
    """
    Tests one of our minesweeper states and prints:
        -A visual representation of the state
        -The state's satisfiability
        -The expected result of the state (for pre-defined states)
        -The result calculated by the encoding
        -A prompt to print all of the state variables

    @param state_num: the number of the minesweeper state
    """

    state_num -= 1            # State 1 has index 0, state 2 has index 1, etc
    state = states[state_num] # Gets the state
    create_encoding(state)    # Adds the constraints and state variables
    solution = E.solve()      # Solves the encoding

    # Prints another diagram of the grid if it is a pre-defined state
    # (the completed user-created state is already printed out)
    if state_num < len(states) - 1:
        print_state(state, state_num + 1)

    # Prints if the encoding is satisfiable, the expected result and model result
    print("SATISFIABLE: " + str(E.is_satisfiable()) + "\n")
    if 0 <= state_num < len(states) - 1:
        print("Expected result:", expected[state_num])
    print("Model result: %s\n" % get_solution(solution))

    while True:
        print_solution = input("Would you like to see the full solution states (y/n)? ")
        try:
            print_solution.strip().lower()
            if print_solution == 'y':
                # Prints the solution
                # The format of this is the boolean values of u, m, x and y for
                # each square as well as the s condition value for the middle square
                print("\nSOLUTION:")
                middle_squares = [1, 2, 3]
                for i in middle_squares:
                    for j in middle_squares:
                        num = str(i) + str(j)
                        keyu = "u" + num
                        keym = "m" + num
                        keyx = "x" + num
                        keyy = "y" + num
                        print(keyu, solution[keyu])
                        print(keym, solution[keym])
                        print(keyx, solution[keyx])
                        print(keyy, solution[keyy])
                        if (i == 2 and j == 2):
                            print("s22", solution["s22"])
                        print()
                break
            elif print_solution == 'n':
                break
            else:
                print("Invalid input\n")
        except:
            print("Invalid input\n")


def get_solution(solution):
    """
    Returns the english representation of the solution

    @param solution: a solved 5x5 minesweeper model (using E.solve())
    @return 'schrodinger's mine': if the middle square is simulatnaously a mine
                and not a mine (you inputted an impossible state)
            'mine': if the middle square is a mine
            'safe': if the middle square is safe
            'unknown': if the middle square is unknown
            <error message>: if the grid could not be solved or an error occured
                (this should not happen, check constraints if you see this)
    """

    try:
        if solution['m22'] and solution['s22']:
            return "schrodinger's mine"
        if solution['m22']:
            return "mine"
        if solution['s22']:
            return "safe"
        return "unknown"
    except:
        return "error: key 'm22' or 's22' does not exist.\
                Model is not satisfiable or an error occured"


if __name__ == "__main__":
    """
    For testing purposes

    Prompts the user to decide if they want to use a pre-defined state
    or create their own, then solves the given state and outputs the result
    """

    num_states = len(states)
    choice = ''

    # Loops until the user chooses to use a pre-defined state or make their own
    while True:
        choice = input("Would you like to use a pre-defined state? (y/n)? ")
        choice.strip().lower()
        if choice == 'y' or choice == 'n':
            break
        else:
            print("Invalid choice\n")

    if choice == 'y':
        print("Here the the pre-defined states:")
        for i in range(num_states):
            print_state(states[i], i+1)

        while True:
            choice = input("Choose a state between 1 and %d: " %(num_states))
            try: 
                choice = int(choice.strip())
                if 1 <= choice <= num_states:
                    test_state(choice)
                    break
                else:
                    print("Invalid choice\n")
            except:
                print("Invalid choice\n")
    else:
        make_mine_state()