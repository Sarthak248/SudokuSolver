# All necessary libraries to be imported
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# Global variables
number_of_games = int(input("Chosen Difficulty is Evil\nHow many games do you want to be played:"))
total_times = []

# Using Webdriver to open the sudoku link
global driver
driver = webdriver.Chrome(executable_path="C:/softwares/chromedriver_win32/chromedriver.exe")
link = 'https://grid.websudoku.com/?level=4'
driver.get(link)
# driver.maximize_window()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


# **************************************
# ALL FUNCTIONS RELATED TO WEB SCRAPING/SELENIUM
# **************************************

# Function to get the 81-digit string from an HTML page source
def get_string():
    page_source = driver.page_source
    sudoku_string = ''
    soup = bs4.BeautifulSoup(page_source, "lxml")
    row1 = soup.find_all('table')
    temp = row1[2]
    t2 = temp.find_all_next('div')
    my_line = t2[2]
    cells = my_line.find_all_next('td')
    for x in cells:
        stversion = str(x)
        if stversion.count('s0') != 0:
            sudoku_string = sudoku_string + stversion[-9]
        else:
            sudoku_string = sudoku_string + '0'
    return sudoku_string


# Function to show the timer as the puzzle is being solved
def show_time():
    time.sleep(1)
    driver.find_element(By.NAME, "showopts").click()
    time.sleep(1)
    driver.find_element(By.NAME, "options1").click()
    time.sleep(1)
    driver.find_element(By.NAME, "saveopts").click()
    time.sleep(1)


# Once the puzzle has been solved using the algorithm, this function displays it on the browser using Selenium
def output(solved_sudoku_string):
    ctr = 0
    i = 0
    j = 0
    my_element = ''
    while ctr < 81:
        if ctr % 9 == 0 and ctr != 0:
            j = j + 1
            i = 0
        my_id = 'f' + str(i) + str(j)
        my_element = driver.find_element(By.ID, my_id)
        my_element.send_keys(solved_sudoku_string[ctr])
        ctr = ctr + 1
        i = i + 1
    time_taken = driver.find_element(By.NAME, "jstimer")
    total_times.append(time_taken.get_attribute('value'))
    time.sleep(3)
    my_element.send_keys(Keys.RETURN)

# **************************************
# ALL FUNCTIONS RELATED TO THE ALGORITHM
# **************************************


# Function to covert an 81-digit string to a 2D array/ Sudoku board
def convert_num_to_board(num):
    # 032000080865900000010020903090408070300562008050109030501090040000004751070000820
    my_board = []
    row = []
    row2 = []
    for i in range(81):
        row.append(int(num[i]))
        if (i+1) % 9 == 0 and i != 0:
            row2 = row.copy()
            my_board.append(row2)
            row.clear()
    return my_board


# Function to check whether the board abides by the rules pertaining to the specific number at the specific position
def check_valid(my_board, num, pos):
    # Check in row
    for i in range(len(my_board[0])):
        if my_board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check in column
    for i in range(len(my_board)):
        if my_board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check in 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if my_board[i][j] == num and (i, j) != pos:
                return False

    return True


# The function that uses backtracking algorithm to recursively call itself and solve the board
# Each empty cell is filled from numbers 1-9 and check_valid() function is called each time
# If it isn't valid, the next number is chosen
# If it is valid, the function is called again to fill the next empty cell and so on

def solve_board(my_board):
    find = find_empty_key(my_board)
    if not find:
        return True
    else:
        row, col = find[0], find[1]
    for temp in range(1, 10):
        if check_valid(my_board, temp, (row, col)):
            my_board[row][col] = temp
            if solve_board(my_board):
                return True
            my_board[row][col] = 0
    return False


# Function to print board
def print_board(my_board):
    for i in range(9):
        for j in range(9):
            print(my_board[i][j], end=" ")
            if (j+1) % 3 == 0 and j != 0 and j != 8:
                print(" | ", end="")
        print()
        if (i+1) % 3 == 0 and i != 0 and i != 8:
            print("_ _ _ _ _ _ _ _ _ _ _ _")


# Function to find an empty cell (0); if true, returns the row-and-cell #; if false, returns False
def find_empty_key(my_board):
    for i in range(9):
        for j in range(9):
            if my_board[i][j] == 0:
                return i, j
    return False


# Function to convert a 2D array/Sudoku board into an 81-digit string
def convert_board_to_num(my_board):
    solved_string = ''
    for i in my_board:
        for j in i:
            solved_string = solved_string + str(j)
    return solved_string


# **************************************
# MAIN
# **************************************

# Main function that runs the game
def call_all_functions():
    unsolved = get_string()
    board = convert_num_to_board(unsolved)
    solve_board(board)
    solved = convert_board_to_num(board)
    output(solved)


show_time()
my_ctr = 0
# User has option to run the game multiple times
while my_ctr < number_of_games:
    if my_ctr != 0:
        driver.find_element(By.NAME, "newgame").click()
        time.sleep(1)
    call_all_functions()
    my_ctr = my_ctr + 1
time.sleep(2)
driver.close()

# Displays efficiency of the algorithm and the program by showing average time taken to solve the puzzle on EVIL mode
sum_of_times = 0
for x in total_times:
    sum_of_times = sum_of_times + int(x)

# 3 time.sleep(1) functions in show_time()
avg_time = sum_of_times / number_of_games - 3
print("The average time to solve the puzzles was:", avg_time, " seconds")
