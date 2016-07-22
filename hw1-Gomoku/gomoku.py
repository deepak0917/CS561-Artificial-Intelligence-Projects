import re
import sys

input_data = open("input_1.txt", 'r')
# inputFile = open(sys.argv[1], "r")
task_type = int(input_data.readline())
twoplayers = {
    1: 'b',
    2: 'w'}

num_player = int(input_data.readline())
depth = int(input_data.readline())
lines_matrix = int(input_data.readline())
currentBoardState = []
nextStatefile = open("./next_state.txt", 'w+')
traverse_2_3 = open("./traverse_log.txt", "w+")

FiveThousand = 5000
TenThousand = 10000
FiftyThousand = 50000
Thousand = 1000
Infinity = "Infinity"
NegativeInfinity = "-Infinity"

dict_col = {}

def initializeNametoColumn():
    start=65
    end=90
    for i in range(0,25):
        dict_col[(i+65)-64]=chr(i+65)

initializeNametoColumn()


def IsBlockedFour(anotherboardstate, point1, point2, currentplayer):
    settotrue = 0
    evaluatethisgo = False
    if point1 + 5 < lines_matrix and point2 + 5 < lines_matrix:
        if anotherboardstate[point1 + 5][point2 + 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif (point1 + 5 == lines_matrix and point2 + 5 <= lines_matrix) or (point1 + 5 <= lines_matrix and point2 + 5 == lines_matrix):
        evaluatethisgo = True

    if evaluatethisgo:
        for var in range(1, 5):
            if not (anotherboardstate[point1 + var][point2 + var] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point1 - 5 >= 0 and point2 - 5 >= 0:
        if anotherboardstate[point1 - 5][point2 - 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif point1 - 5 == -1 or point2 - 5 == -1:
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1 - var2][point2 - var2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False

    if point1 - 5 >= 0:
        if anotherboardstate[point1 - 5][point2] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif point1 - 5 == -1:
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1 - var2][point2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point2 + 5 < lines_matrix:
        if anotherboardstate[point1][point2 + 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif point2 + 5 == lines_matrix:
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1][point2 + var2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point1 + 5 < lines_matrix:
        if anotherboardstate[point1 + 5][point2] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif point1 + 5 == lines_matrix:
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1 + var2][point2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point2 - 5 >= 0:
        if anotherboardstate[point1][point2 - 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif point2 - 5 == -1:
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1][point2 - var2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point1 + 5 < lines_matrix and point2 - 5 >= 0:
        if anotherboardstate[point1 + 5][point2 - 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif (point1 + 5 == lines_matrix and point2 - 5 >= -1) or (point1 + 5 <= lines_matrix and point2 - 5 == -1):
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1 + var2][point2 - var2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    evaluatethisgo = False
    if point1 - 5 >= 0 and point2 + 5 < lines_matrix:
        if anotherboardstate[point1 - 5][point2 + 5] == twoplayers[currentplayer]:
            evaluatethisgo = True
    elif (point1 - 5 == -1 and point2 + 5 <= lines_matrix) or (point1 - 5 >= -1 and point2 + 5 == lines_matrix):
        evaluatethisgo = True

    if evaluatethisgo:
        for var2 in range(1, 5):
            if not (anotherboardstate[point1 - var2][point2 + var2] == twoplayers[3 - currentplayer]):
                break
        else:
            settotrue += 1

    return settotrue
def ReverseBoard(justboard):
    justboard.reverse()
    return justboard


def Board_create_func(dimension, val):
    ReturnthisBoard=[]
    for i in range(0, dimension):
        templine=input_data.readline()
        currentBoardState.append(templine)
    ReturnthisBoard=ReverseBoard(currentBoardState)
    return ReturnthisBoard


Board_create_func(lines_matrix,1)

def IsClosedFour(board, point1, point2, playerone):
    isititrue = 0

    count = 0
    for var2 in range(-4, 5):
        if point1+var2 >= 0 and point1+var2 < lines_matrix and point2+var2 >= 0 and point2+var2 < lines_matrix:
            if var2 == 0 or (board[point1 + var2][point2 + var2] == twoplayers[playerone]):
                if count == 4:
                    count = 0
                else:
                    count += 1
            else:
                if count == 4:
                    if board[point1 + var2][point2 + var2] == twoplayers[3 - playerone]:
                        if point1 + var2 - 5 >= 0 and point2 + var2 - 5 >= 0:
                            if board[point1 + var2 - 5][point2 + var2 - 5] == '.':
                                isititrue += 1
                                break
                            else:
                                count = 0
                        else:
                            count = 0
                    elif board[point1 + var2][point2 + var2] == '.':
                        if point1 + var2 - 5 >= 0 and point2 + var2 - 5 >= 0:
                            if board[point1 + var2 - 5][point2 + var2 - 5] == twoplayers[3 - playerone]:
                                isititrue += 1
                                break
                            else:
                                count = 0
                        elif point1 + var2 - 5 == -1 or point2 + var2 - 5 == -1:
                            isititrue += 1
                            break
                        else:
                            count = 0
                else:
                    count = 0
        elif point1 + var2 == lines_matrix or point2 + var2 == lines_matrix:
            if count == 4 and board[point1 + var2 - 5][point2 + var2 - 5] == '.':
                if point1 + var2 - 5 >= 0 and point2 + var2 - 5 >= 0:
                    isititrue += 1
                    break

    count = 0
    for var2 in range(-4, 5):
        if point1+var2 >= 0 and point1+var2 < lines_matrix and point2-var2 >= 0 and point2-var2 < lines_matrix:
            if var2 == 0 or (board[point1 + var2][point2 - var2] == twoplayers[playerone]):
                if count == 4:
                    count = 0
                else:
                    count += 1
            else:
                if count == 4:
                    if board[point1 + var2][point2 - var2] == twoplayers[3 - playerone]:
                        if point1 + var2 - 5 >= 0 and point2 - var2 + 5 >= 0:
                            if board[point1 + var2 - 5][point2 - var2 + 5] == '.':
                                isititrue += 1
                                break
                            else:
                                count = 0
                        else:
                            count = 0
                    elif board[point1 + var2][point2 - var2] == '.':
                        if point1 + var2 - 5 >= 0 and point2 - var2 + 5 < lines_matrix:
                            if board[point1 + var2 - 5][point2 - var2 + 5] == twoplayers[3 - playerone]:
                                isititrue += 1
                                break
                            else:
                                count = 0
                        elif point1 + var2 - 5 == -1 or point2 - var2 + 5 == lines_matrix:
                            isititrue += 1
                            break
                        else:
                            count = 0
                else:
                    count = 0
        elif point1 + var2 == lines_matrix or point2 - var2 == -1:
            if count == 4 and board[point1 + var2 - 5][point2 - var2 + 5] == '.':
                if point1 + var2 - 5 >= 0 and point2 - var2 + 5 < lines_matrix:
                    isititrue += 1
                    break

    count = 0
    for var2 in range(-4, 5):
        if point1 >= 0 and point1 < lines_matrix and point2+var2 >= 0 and point2+var2 < lines_matrix:
            if var2 == 0 or (board[point1][point2 + var2] == twoplayers[playerone]):
                if count == 4:
                    count = 0
                else:
                    count += 1
            else:
                if count == 4:
                    if board[point1][point2 + var2] == twoplayers[3 - playerone]:
                        if point2 + var2 - 5 >= 0:
                            if board[point1][point2 + var2 - 5] == '.':
                                isititrue += 1
                                break
                            else:
                                count = 0
                        else:
                            count = 0
                    elif board[point1][point2 + var2] == '.':
                        if point2 + var2 - 5 >= 0:
                            if board[point1][point2 + var2 - 5] == twoplayers[3 - playerone]:
                                isititrue += 1
                                break
                            else:
                                count = 0
                        elif point2 + var2 - 5 == -1:
                            isititrue += 1
                            break
                        else:
                            count = 0
                else:
                    count = 0
        elif point2 + var2 == lines_matrix:
            if count == 4 and board[point1][point2 + var2 - 5] == '.':
                if point2 + var2 - 5 >= 0:
                    isititrue += 1
                    break

    count = 0
    for var2 in range(-4, 5):
        if point1+var2 >= 0 and point1+var2 < lines_matrix and point2 >= 0 and point2 < lines_matrix:
            if var2 == 0 or (board[point1 + var2][point2] == twoplayers[playerone]):
                if count == 4:
                    count = 0
                else:
                    count += 1
            else:
                if count == 4:
                    if board[point1 + var2][point2] == twoplayers[3 - playerone]:
                        if point1 + var2 - 5 >= 0:
                            if board[point1 + var2 - 5][point2] == '.':
                                isititrue += 1
                                break
                            else:
                                count = 0
                        else:
                            count = 0
                    elif board[point1 + var2][point2] == '.':
                        if point1 + var2 - 5 >= 0:
                            if board[point1 + var2 - 5][point2] == twoplayers[3 - playerone]:
                                isititrue += 1
                                break
                            else:
                                count = 0
                        elif point1 + var2 - 5 == -1:
                            isititrue += 1
                            break
                        else:
                            count = 0
                else:
                    count = 0
        elif point1 + var2 == lines_matrix:
            if count == 4 and board[point1 + var2 - 5][point2] == '.':
                if point1 + var2 - 5 >= 0:
                    isititrue += 1
                    break
    return isititrue

def legalize_moves(i, j):
    IsTrue=0
    if i >= 0 and i < lines_matrix and j >= 0 and j < lines_matrix:
        IsTrue=1
    else:
        IsTrue =0
    return True if(IsTrue==1) else False


def find_possible_moves_l(board_pos, line):
    l_moves = []
    for i in range(0, lines_matrix):
        for j in range(0, lines_matrix):
            if board_pos[i][j] == '.':
                continue
            else:
                if i >= 0 and i < lines_matrix and j-1 >= 0 and j-1 < lines_matrix:
                    l_moves = move_legal(l_moves, i, j - 1, board_pos)

                if i-1 >= 0 and i-1 < lines_matrix and j-1 >= 0 and j-1 < lines_matrix:
                    l_moves = move_legal(l_moves, i - 1, j - 1, board_pos)

                if i-1 >= 0 and i-1 < lines_matrix and j >= 0 and j < lines_matrix:
                    l_moves = move_legal(l_moves, i - 1, j, board_pos)

                if i-1 >= 0 and i-1 < lines_matrix and j+1 >= 0 and j+1 < lines_matrix:
                    l_moves = move_legal(l_moves, i - 1, j + 1, board_pos)

                if i >= 0 and i < lines_matrix and j+1 >= 0 and j+1 < lines_matrix:
                    l_moves = move_legal(l_moves, i, j + 1, board_pos)

                if i+1 >= 0 and i+1 < lines_matrix and j+1 >= 0 and j+1 < lines_matrix:
                    l_moves = move_legal(l_moves, i + 1, j + 1, board_pos)

                if i+1 >= 0 and i+1 < lines_matrix and j >= 0 and j < lines_matrix:
                    l_moves = move_legal(l_moves, i + 1, j, board_pos)

                if i+1 >= 0 and i+1 < lines_matrix and j-1 >= 0 and j-1 < lines_matrix:
                    l_moves = move_legal(l_moves, i + 1, j - 1, board_pos)

    return l_moves

def create_closed_two(board1, point1, point2, player1):
    isittrue = 0

    totalcount = 0
    for var6 in range(-2, 3):
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2+var6 >= 0 and point2+var6 < lines_matrix:
            if var6 == 0 or (board1[point1 + var6][point2 + var6] == twoplayers[player1]):
                if totalcount == 2:
                    totalcount = 0
                else:
                    totalcount += 1
            else:
                if totalcount == 2:
                    if board1[point1 + var6][point2 + var6] == twoplayers[3 - player1]:
                        if point1 + var6 - 3 >= 0 and point2 + var6 - 3 >= 0:
                            if board1[point1 + var6 - 3][point2 + var6 - 3] == '.':
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        else:
                            totalcount = 0
                    elif board1[point1 + var6][point2 + var6] == '.':
                        if point1 + var6 - 3 >= 0 and point2 + var6 - 3 >= 0:
                            if board1[point1 + var6 - 3][point2 + var6 - 3] == twoplayers[3 - player1]:
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        elif point1 + var6 - 3 == -1 or point2 + var6 - 3 == -1:
                            isittrue += 1
                            break
                        else:
                            totalcount = 0
                else:
                    totalcount = 0
        elif point1 + var6 == lines_matrix or point2 + var6 == lines_matrix:
            if totalcount == 2 and board1[point1 + var6 - 3][point2 + var6 - 3] == '.':
                if point1 + var6 - 3 >= 0 and point2 + var6 - 3 >= 0:
                    isittrue += 1
                    break

    totalcount = 0
    for var6 in range(-2, 3):
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2-var6 >= 0 and point2-var6 < lines_matrix:
            if var6 == 0 or (board1[point1 + var6][point2 - var6] == twoplayers[player1]):
                if totalcount == 2:
                    totalcount = 0
                else:
                    totalcount += 1
            else:
                if totalcount == 2:
                    if board1[point1 + var6][point2 - var6] == twoplayers[3 - player1]:
                        if point1 + var6 - 3 >= 0 and point2 - var6 + 3 >= 0:
                            if board1[point1 + var6 - 3][point2 - var6 + 3] == '.':
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        else:
                            totalcount = 0
                    elif board1[point1 + var6][point2 - var6] == '.':
                        if point1 + var6 - 3 >= 0 and point2 - var6 + 3 < lines_matrix:
                            if board1[point1 + var6 - 3][point2 - var6 + 3] == twoplayers[3 - player1]:
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        elif point1 + var6 - 3 == -1 or point2 - var6 + 3 == lines_matrix:
                            isittrue += 1
                            break
                        else:
                            totalcount = 0
                else:
                    totalcount = 0
        elif point1 + var6 == lines_matrix or point2 - var6 == -1:
            if totalcount == 2 and board1[point1 + var6 - 3][point2 - var6 + 3] == '.':
                if point1 + var6 - 3 >= 0 and point2 - var6 + 3 < lines_matrix:
                    isittrue += 1
                    break

    totalcount = 0
    for var6 in range(-2, 3):  # Check for horizontal
        if point1 >= 0 and point1 < lines_matrix and point2+var6 >= 0 and point2+var6 < lines_matrix:
            if var6 == 0 or (board1[point1][point2 + var6] == twoplayers[player1]):
                if totalcount == 2:
                    totalcount = 0
                else:
                    totalcount += 1
            else:
                if totalcount == 2:
                    if board1[point1][point2 + var6] == twoplayers[3 - player1]:
                        if point2 + var6 - 3 >= 0:
                            if board1[point1][point2 + var6 - 3] == '.':
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        else:
                            totalcount = 0
                    elif board1[point1][point2 + var6] == '.':
                        if point2 + var6 - 3 >= 0:
                            if board1[point1][point2 + var6 - 3] == twoplayers[3 - player1]:
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        elif point2 + var6 - 3 == -1:
                            isittrue += 1
                            break
                        else:
                            totalcount = 0
                else:
                    totalcount = 0
        elif point2 + var6 == lines_matrix:
            if totalcount == 2 and board1[point1][point2 + var6 - 3] == '.':
                if point2 + var6 - 3 >= 0:
                    isittrue += 1
                    break

    totalcount = 0
    for var6 in range(-2, 3):  # Check for vertical
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2 >= 0 and point2 < lines_matrix:
            if var6 == 0 or board1[point1 + var6][point2] == twoplayers[player1]:
                if totalcount == 2:
                    totalcount = 0
                else:
                    totalcount += 1
            else:
                if totalcount == 2:
                    if board1[point1 + var6][point2] == twoplayers[3 - player1]:
                        if point1 + var6 - 3 >= 0:
                            if board1[point1 + var6 - 3][point2] == '.':
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        else:
                            totalcount = 0
                    elif board1[point1 + var6][point2] == '.':
                        if point1 + var6 - 3 >= 0:
                            if board1[point1 + var6 - 3][point2] == twoplayers[3 - player1]:
                                isittrue += 1
                                break
                            else:
                                totalcount = 0
                        elif point1 + var6 - 3 == -1:
                            isittrue += 1
                            break
                        else:
                            totalcount = 0
                else:
                    totalcount = 0
        elif point1 + var6 == lines_matrix:
            if totalcount == 2 and board1[point1 + var6 - 3][point2] == '.':
                if point1 + var6 - 3 >= 0:
                    isittrue += 1
                    break
    return isittrue

def move_legal(lmoves, i, j, bord):
    if bord[i][j] == ".":
        one_movement = dict_col[j + 1] + str(i + 1)
        if one_movement not in lmoves:
            lmoves.append(one_movement)
    return lmoves


def sorting_moves(move):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    move.sort(key=alphanum_key)
    return move


def convert_alpha_to_index(tempsteps):
    indexing = []
    alphauniquekey = tempsteps[:1]
    for i in dict_col:
        if dict_col[i] == alphauniquekey:
            indexing.append(i - 1)
    indexing.append((int(tempsteps[1:]) - 1))

    return indexing

def AddMyTotal(Total,num1,num2):
    return Total + (num1 *num2)

def evaluation_function(someboard, steps, current_player):

    index = convert_alpha_to_index(steps)
    won = win(someboard, index[1], index[0], current_player)
    Total_score = 0
    if won > 0:
        Total_score=AddMyTotal(Total_score,FiftyThousand,won)
    variable4 = IsBlockedFour(someboard, index[1], index[0], current_player)
    if variable4 > 0:
        Total_score=AddMyTotal(Total_score,TenThousand,variable4)
    closedopenfour = IsOpenFour(someboard, index[1], index[0], current_player)
    if closedopenfour > 0:
        Total_score = AddMyTotal(Total_score,FiveThousand,closedopenfour)
    closedclosedthree = IsClosedFour(someboard, index[1], index[0], current_player)
    if closedclosedthree > 0:
        Total_score = AddMyTotal(Total_score,Thousand,closedclosedthree)
    bothopenthree = IsBlockedOpenThree(someboard, index[1], index[0], current_player)
    if bothopenthree > 0:
        Total_score = AddMyTotal(Total_score,500,bothopenthree)
    bothclosethree = IsBlockedClosedThree(someboard, index[1], index[0], current_player)
    if bothclosethree > 0:
        Total_score = AddMyTotal(Total_score,100,bothclosethree)
    closeopen3 = Iscreateopenthree(someboard, index[1], index[0], current_player)
    if closeopen3 > 0:
        Total_score = AddMyTotal(Total_score,50,closeopen3)
    variablelcosethree = iscreateclosedthree(someboard, index[1], index[0], current_player)
    if variablelcosethree > 0:
        Total_score = AddMyTotal(Total_score,10,variablelcosethree)
    closeopenthwo = create_open_two(someboard, index[1], index[0], current_player)
    if closeopenthwo > 0:
        Total_score = AddMyTotal(Total_score,5,closeopenthwo)
    closeclosetwo = create_closed_two(someboard, index[1], index[0], current_player)
    if closeclosetwo > 0:
        Total_score += 1 * closeclosetwo
    return Total_score


def greedyfunctioncalling(greedyboard, steps):
    max_evaluationvariable = sys.maxsize * -1
    finalgreedymove = None
    finalgreedymove = ""
    for j in steps:
        score = evaluation_function(greedyboard, j, num_player)
        if score > max_evaluationvariable:
            max_evaluationvariable = score
            finalgreedymove = j
    boardtofile(finalgreedymove, num_player)
    return max_evaluationvariable


def boardtofile(finalstepstobeperformed, unknownp):
    index = convert_alpha_to_index(finalstepstobeperformed)
    for i in range(lines_matrix - 1, -1, -1):
        for j in range(0, lines_matrix):
            if not (index[1] == i and index[0] == j):
                nextStatefile.write(currentBoardState[i][j])
            else:
                nextStatefile.write(twoplayers[unknownp])
        nextStatefile.write('\n')
    nextStatefile.close()


def win(board, i, j, p):
    won = 0

    count = 0
    for m in range(-4, 5):
        if i+m >= 0 and i+m < lines_matrix and j+m >= 0 and j+m < lines_matrix:
            if m == 0 or board[i + m][j + m] == twoplayers[p]:
                count += 1
            else:
                count = 0
        else:
            count = 0
        if count == 5:
            won += 1
            break
    count = 0
    for m in range(-4, 5):
        if i+m >= 0 and i+m < lines_matrix and j-m >= 0 and j-m < lines_matrix:
            if m == 0 or board[i + m][j - m] == twoplayers[p]:
                count += 1
            else:
                count = 0
        else:
            count = 0
        if count == 5:
            won += 1
            break
    count = 0
    for m in range(-4, 5):
        if i-m >= 0 and i-m < lines_matrix and j >= 0 and j < lines_matrix:
            if m == 0 or board[i - m][j] == twoplayers[p]:
                count += 1
            else:
                count = 0
        else:
            count = 0
        if count == 5:
            won += 1
            break
    count = 0
    for m in range(-4, 5):
        if i >= 0 and i < lines_matrix and j-m >= 0 and j-m < lines_matrix:
            if m == 0 or board[i][j - m] == twoplayers[p]:
                count += 1
            else:
                count = 0
        else:
            count = 0
        if count == 5:
            won += 1
            break
    return won





def IsOpenFour(thisiscurrentboard, point1, point2, playerone):
    isittrue = 0
    total = 0
    for var1 in range(-4, 5):
        if point1+var1 >= 0 and point1+var1 < lines_matrix and point2 >= 0 and point2 < lines_matrix:
            if thisiscurrentboard[point1 + var1][point2] == twoplayers[playerone] or var1 == 0:
                total += 1
            elif thisiscurrentboard[point1 + var1][point2] == twoplayers[3 - playerone]:
                total = 0
            elif thisiscurrentboard[point1 + var1][point2] == '.':
                if total == 5 and legalize_moves(point1 + var1 - 5, point2) and thisiscurrentboard[point1 + var1 - 5][point2] == ".":
                    isittrue += 1
                else:
                    total = 1
    total = 0
    for var1 in range(-4, 5):
        if point1+var1 >= 0 and point1+var1 < lines_matrix and point2+var1 >= 0 and point2+var1 < lines_matrix:
            if thisiscurrentboard[point1 + var1][point2 + var1] == twoplayers[playerone] or var1 == 0:
                total += 1
            elif thisiscurrentboard[point1 + var1][point2 + var1] == twoplayers[3 - playerone]:
                total = 0
            elif thisiscurrentboard[point1 + var1][point2 + var1] == '.':
                if total == 5 and legalize_moves(point1 + var1 - 5, point2 + var1 - 5) and thisiscurrentboard[point1 + var1 - 5][point2 + var1 - 5] == ".":
                    isittrue += 1
                else:
                    total = 1
    total = 0
    for var1 in range(-4, 5):
        if point1+var1 >= 0 and point1+var1 < lines_matrix and point2-var1 >= 0 and point2-var1 < lines_matrix:
            if thisiscurrentboard[point1 + var1][point2 - var1] == twoplayers[playerone] or var1 == 0:
                total += 1
            elif thisiscurrentboard[point1 + var1][point2 - var1] == twoplayers[3 - playerone]:
                total = 0
            elif thisiscurrentboard[point1 + var1][point2 - var1] == '.':
                if total == 5 and legalize_moves(point1 + var1 - 5, point2 - var1 + 5) and thisiscurrentboard[point1 + var1 - 5][point2 - var1 + 5] == ".":
                    isittrue += 1
                else:
                    total = 1
    total = 0
    for var1 in range(-4, 5):
        if point1 >= 0 and point1 < lines_matrix and point2+var1 >= 0 and point2+var1 < lines_matrix:
            if thisiscurrentboard[point1][point2 + var1] == twoplayers[playerone] or var1 == 0:
                total += 1
            elif thisiscurrentboard[point1][point2 + var1] == twoplayers[3 - playerone]:
                total = 0
            elif thisiscurrentboard[point1][point2 + var1] == '.':
                if total == 5 and legalize_moves(point1, point2 + var1 - 5) and thisiscurrentboard[point1][point2 + var1 - 5] == ".":
                    isittrue += 1
                else:
                    total = 1
    return isittrue



def IsBlockedOpenThree(board, point1, point2, playerone):
    isittrue = 0

    variable2 = False
    if point1 + 4 < lines_matrix and point2 + 4 < lines_matrix:
        if board[point1 + 4][point2 + 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not board[point1 + m][point2 + m] == twoplayers[3 - playerone]:
                break
        else:
            isittrue += 1

    variable2 = False
    if point1 - 4 >= 0 and point2 - 4 >= 0:
        if board[point1 - 4][point2 - 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not board[point1 - m][point2 - m] == twoplayers[3 - playerone]:
                break
        else:
            isittrue += 1

    variable2 = False  # Check horizontal left
    if point2 - 4 >= 0:
        if board[point1][point2 - 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1][point2 - m] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    variable2 = False
    if point2 + 4 < lines_matrix:
        if board[point1][point2 + 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1][point2 + m] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    variable2 = False
    if point1 - 4 >= 0:
        if board[point1 - 4][point2] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1 - m][point2] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    variable2 = False
    if point1 + 4 < lines_matrix:
        if board[point1 + 4][point2] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1 + m][point2] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    variable2 = False  # Check for a diagonal
    if point1 + 4 < lines_matrix and point2 - 4 >= 0:
        if board[point1 + 4][point2 - 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1 + m][point2 - m] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    variable2 = False
    if point1 - 4 >= 0 and point2 + 4 < lines_matrix:
        if board[point1 - 4][point2 + 4] == ".":
            variable2 = True

    if variable2:
        for m in range(1, 4):
            if not (board[point1 - m][point2 + m] == twoplayers[3 - playerone]):
                break
        else:
            isittrue += 1

    return isittrue

def IsBlockedClosedThree(theboard, point1, point2, playerone1):
    isititrue = 0

    check = False
    if point1 + 4 < lines_matrix and point2 + 4 < lines_matrix:
        if theboard[point1 + 4][point2 + 4] == twoplayers[playerone1]:
            check = True
    elif (point1 + 4 == lines_matrix and point2 + 4 <= lines_matrix) or (point1 + 4 <= lines_matrix and point2 + 4 == lines_matrix):
        check = True

    if check:
        for var3 in range(1, 4):
            if not theboard[point1 + var3][point2 + var3] == twoplayers[3 - playerone1]:
                break
        else:
            isititrue += 1

    check = False
    if point1 - 4 >= 0 and point2 - 4 >= 0:
        if theboard[point1 - 4][point2 - 4] == twoplayers[playerone1]:
            check = True
    elif (point1 - 4 == -1 and point2 - 4 >= -1) or (point1 - 4 >= -1 and point2 - 4 == -1):
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1 - var3][point2 - var3] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point1 - 4 >= 0:
        if theboard[point1 - 4][point2] == twoplayers[playerone1]:
            check = True
    elif point1 - 4 == -1:
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1 - var3][point2] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point2 + 4 < lines_matrix:
        if theboard[point1][point2 + 4] == twoplayers[playerone1]:
            check = True
    elif point2 + 4 == lines_matrix:
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1][point2 + var3] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point1 + 4 < lines_matrix:
        if theboard[point1 + 4][point2] == twoplayers[playerone1]:
            check = True
    elif point1 + 4 == lines_matrix:
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1 + var3][point2] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point2 - 4 >= 0:
        if theboard[point1][point2 - 4] == twoplayers[playerone1]:
            check = True
    elif point2 - 4 == -1:
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1][point2 - var3] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point1 + 4 < lines_matrix and point2 - 4 >= 0:
        if theboard[point1 + 4][point2 - 4] == twoplayers[playerone1]:
            check = True
    elif (point1 + 4 == lines_matrix and point2 - 4 >= -1) or (point1 + 4 <= lines_matrix and point2 - 4 == -1):
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1 + var3][point2 - var3] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    check = False
    if point1 - 4 >= 0 and point2 + 4 < lines_matrix:
        if theboard[point1 - 4][point2 + 4] == twoplayers[playerone1]:
            check = True
    elif (point1 - 4 == -1 and point2 + 4 <= lines_matrix) or (point1 - 4 >= -1 and point2 + 4 == lines_matrix):
        check = True

    if check:
        for var3 in range(1, 4):
            if not (theboard[point1 - var3][point2 + var3] == twoplayers[3 - playerone1]):
                break
        else:
            isititrue += 1

    return isititrue

def Iscreateopenthree(boarstates, point1, point2, playerone):
    isititrue = 0

    count = 0
    for var4 in range(-3, 4):
        if point1+var4 >= 0 and point1+var4 < lines_matrix and point2 >= 0 and point2 < lines_matrix:
            if boarstates[point1 + var4][point2] == twoplayers[playerone] or var4 == 0:
                count += 1
            elif boarstates[point1 + var4][point2] == twoplayers[3 - playerone]:
                count = 0
            elif boarstates[point1 + var4][point2] == '.':
                if count == 4 and legalize_moves(point1 + var4 - 4, point2) and boarstates[point1 + var4 - 4][point2] == ".":
                    isititrue += 1
                else:
                    count = 1
    count = 0
    for var4 in range(-3, 4):
        if point1+var4 >= 0 and point1+var4 < lines_matrix and point2+var4 >= 0 and point2+var4 < lines_matrix:
            if boarstates[point1 + var4][point2 + var4] == twoplayers[playerone] or var4 == 0:
                count += 1
            elif boarstates[point1 + var4][point2 + var4] == twoplayers[3 - playerone]:
                count = 0
            elif boarstates[point1 + var4][point2 + var4] == '.':
                if count == 4 and legalize_moves(point1 + var4 - 4, point2 + var4 - 4) and boarstates[point1 + var4 - 4][
                                    point2 + var4 - 4] == ".":
                    isititrue += 1
                else:
                    count = 1
    count = 0
    for var4 in range(-3, 4):
        if point1+var4 >= 0 and point1+var4 < lines_matrix and point2-var4 >= 0 and point2-var4 < lines_matrix:
            if boarstates[point1 + var4][point2 - var4] == twoplayers[playerone] or var4 == 0:
                count += 1
            elif boarstates[point1 + var4][point2 - var4] == twoplayers[3 - playerone]:
                count = 0
            elif boarstates[point1 + var4][point2 - var4] == '.':
                if count == 4 and legalize_moves(point1 + var4 - 4, point2 - var4 + 4) and boarstates[point1 + var4 - 4][point2 - var4 + 4] == ".":
                    isititrue += 1
                else:
                    count = 1
    count = 0
    for var4 in range(-3, 4):
        if point1 >= 0 and point1 < lines_matrix and point2+var4 >= 0 and point2+var4 < lines_matrix:
            if boarstates[point1][point2 + var4] == twoplayers[playerone] or var4 == 0:
                count += 1
            elif boarstates[point1][point2 + var4] == twoplayers[3 - playerone]:
                count = 0
            elif boarstates[point1][point2 + var4] == '.':
                if count == 4 and legalize_moves(point1, point2 + var4 - 4) and boarstates[point1][point2 + var4 - 4] == ".":
                    isititrue += 1
                else:
                    count = 1
    return isititrue

def iscreateclosedthree(board, i, j, p):
    found = 0

    totalvarlue = 0
    for var5 in range(-3, 4):
        if i+var5 >= 0 and i+var5 < lines_matrix and j+var5 >= 0 and j+var5 < lines_matrix:
            if var5 == 0 or (board[i + var5][j + var5] == twoplayers[p]):
                if totalvarlue == 3:
                    totalvarlue = 0
                else:
                    totalvarlue += 1
            else:
                if totalvarlue == 3:
                    if board[i + var5][j + var5] == twoplayers[3 - p]:
                        if i + var5 - 4 >= 0 and j + var5 - 4 >= 0:
                            if board[i + var5 - 4][j + var5 - 4] == '.':
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        else:
                            totalvarlue = 0
                    elif board[i + var5][j + var5] == '.':
                        if i + var5 - 4 >= 0 and j + var5 - 4 >= 0:
                            if board[i + var5 - 4][j + var5 - 4] == twoplayers[3 - p]:
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        elif i + var5 - 4 == -1 or j + var5 - 4 == -1:
                            found += 1
                            break
                        else:
                            totalvarlue = 0
                else:
                    totalvarlue = 0
        elif i + var5 == lines_matrix or j + var5 == lines_matrix:
            if totalvarlue == 3 and board[i + var5 - 4][j + var5 - 4] == '.':
                if i + var5 - 4 >= 0 and j + var5 - 4 >= 0:
                    found += 1
                    break

    totalvarlue = 0
    for var5 in range(-3, 4):
        if i+var5 >= 0 and i+var5 < lines_matrix and j-var5 >= 0 and j-var5 < lines_matrix:
            if var5 == 0 or (board[i + var5][j - var5] == twoplayers[p]):
                if totalvarlue == 3:
                    totalvarlue = 0
                else:
                    totalvarlue += 1
            else:
                if totalvarlue == 3:
                    if board[i + var5][j - var5] == twoplayers[3 - p]:
                        if i + var5 - 4 >= 0 and j - var5 + 4 >= 0:
                            if board[i + var5 - 4][j - var5 + 4] == '.':
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        else:
                            totalvarlue = 0
                    elif board[i + var5][j - var5] == '.':
                        if i + var5 - 4 >= 0 and j - var5 + 4 < lines_matrix:
                            if board[i + var5 - 4][j - var5 + 4] == twoplayers[3 - p]:
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        elif i + var5 - 4 == -1 or j - var5 + 4 == lines_matrix:
                            found += 1
                            break
                        else:
                            totalvarlue = 0
                else:
                    totalvarlue = 0
        elif i + var5 == lines_matrix or j - var5 == -1:
            if totalvarlue == 3 and board[i + var5 - 4][j - var5 + 4] == '.':
                if i + var5 - 4 >= 0 and j - var5 + 4 < lines_matrix:
                    found += 1
                    break

    totalvarlue = 0
    for var5 in range(-3, 4):
        if i >= 0 and i < lines_matrix and j+var5 >= 0 and j+var5 < lines_matrix:
            if var5 == 0 or (board[i][j + var5] == twoplayers[p]):
                if totalvarlue == 3:
                    totalvarlue = 0
                else:
                    totalvarlue += 1
            else:
                if totalvarlue == 3:
                    if board[i][j + var5] == twoplayers[3 - p]:
                        if j + var5 - 4 >= 0:
                            if board[i][j + var5 - 4] == '.':
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        else:
                            totalvarlue = 0
                    elif board[i][j + var5] == '.':
                        if j + var5 - 4 >= 0:
                            if board[i][j + var5 - 4] == twoplayers[3 - p]:
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        elif j + var5 - 4 == -1:
                            found += 1
                            break
                        else:
                            totalvarlue = 0
                else:
                    totalvarlue = 0
        elif j + var5 == lines_matrix:
            if totalvarlue == 3 and board[i][j + var5 - 4] == '.':
                if j + var5 - 4 >= 0:
                    found += 1
                    break

    totalvarlue = 0
    for var5 in range(-3, 4):  # Check for vertical
        if i+var5 >= 0 and i+var5 < lines_matrix and j >= 0 and j < lines_matrix:
            if var5 == 0 or (board[i + var5][j] == twoplayers[p]):
                if totalvarlue == 3:
                    totalvarlue = 0
                else:
                    totalvarlue += 1
            else:
                if totalvarlue == 3:
                    if board[i + var5][j] == twoplayers[3 - p]:
                        if i + var5 - 4 >= 0:
                            if board[i + var5 - 4][j] == '.':
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        else:
                            totalvarlue = 0
                    elif board[i + var5][j] == '.':
                        if i + var5 - 4 >= 0:
                            if board[i + var5 - 4][j] == twoplayers[3 - p]:
                                found += 1
                                break
                            else:
                                totalvarlue = 0
                        elif i + var5 - 4 == -1:
                            found += 1
                            break
                        else:
                            totalvarlue = 0
                else:
                    totalvarlue = 0
        elif i + var5 == lines_matrix:
            if totalvarlue == 3 and board[i + var5 - 4][j] == '.':
                if i + var5 - 4 >= 0:
                    found += 1
                    break
    return found

def create_open_two(board, point1, point2, player1):
    isititrue = 0

    total_value = 0
    for var6 in range(-2, 3):
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2 >= 0 and point2 < lines_matrix:
            if board[point1 + var6][point2] == twoplayers[player1] or var6 == 0:
                total_value += 1
            elif board[point1 + var6][point2] == twoplayers[3 - player1]:
                total_value = 0
            elif board[point1 + var6][point2] == '.':
                if total_value == 3 and legalize_moves(point1 + var6 - 3, point2) and board[point1 + var6 - 3][point2] == ".":
                    isititrue += 1
                else:
                    total_value = 1
    total_value = 0
    for var6 in range(-2, 3):
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2+var6 >= 0 and point2+var6 < lines_matrix:
            if board[point1 + var6][point2 + var6] == twoplayers[player1] or var6 == 0:
                total_value += 1
            elif board[point1 + var6][point2 + var6] == twoplayers[3 - player1]:
                total_value = 0
            elif board[point1 + var6][point2 + var6] == '.':
                if total_value == 3 and legalize_moves(point1 + var6 - 3, point2 + var6 - 3) and board[point1 + var6 - 3][
                                    point2 + var6 - 3] == ".":
                    isititrue += 1
                else:
                    total_value = 1
    total_value = 0
    for var6 in range(-2, 3):
        if point1+var6 >= 0 and point1+var6 < lines_matrix and point2-var6 >= 0 and point2-var6 < lines_matrix:
            if board[point1 + var6][point2 - var6] == twoplayers[player1] or var6 == 0:
                total_value += 1
            elif board[point1 + var6][point2 - var6] == twoplayers[3 - player1]:
                total_value = 0
            elif board[point1 + var6][point2 - var6] == '.':
                if total_value == 3 and legalize_moves(point1 + var6 - 3, point2 - var6 + 3) and board[point1 + var6 - 3][
                                    point2 - var6 + 3] == ".":
                    isititrue += 1
                else:
                    total_value = 1
    total_value = 0
    for var6 in range(-2, 3):
        if point1 >= 0 and point1 < lines_matrix and point2+var6 >= 0 and point2+var6 < lines_matrix:
            if board[point1][point2 + var6] == twoplayers[player1] or var6 == 0:
                total_value += 1
            elif board[point1][point2 + var6] == twoplayers[3 - player1]:
                total_value = 0
            elif board[point1][point2 + var6] == '.':
                if total_value == 3 and legalize_moves(point1, point2 + var6 - 3) and board[point1][point2 + var6 - 3] == ".":
                    isititrue += 1
                else:
                    total_value = 1
    return isititrue


def setplayerandupdateboard(n_board, index_i, index_j, p):
    new_board_with_m = []
    for i in range(0, lines_matrix):
        r = []
        for j in range(0, lines_matrix):
            if not (i == index_i and j == index_j):
                r.append(n_board[i][j])
            else:
                r.append(twoplayers[p])
        new_board_with_m.append(r)
    return new_board_with_m

def findminimumtree(currentboard, steps, localdepth, curentplayer, val):
    if localdepth == depth:
        val = val + evaluation_function(currentboard, steps, curentplayer)
        CallLogging(steps, localdepth, val)
        return val
    else:
        v = sys.maxsize
        val += evaluation_function(currentboard, steps, curentplayer)  # store this somevaluedude for future adding
        index = convert_alpha_to_index(steps)
        updateboard = setplayerandupdateboard(currentboard, index[1], index[0], curentplayer)
        winning = win(currentboard, index[1], index[0], curentplayer)
        if winning > 0:
            CallLogging(steps, localdepth, val)
            return val
        new_moves = find_possible_moves_l(updateboard, lines_matrix)
        new_moves = sorting_moves(new_moves)
        CallLogging(steps, localdepth, Infinity)
        for m in new_moves:
            v = min(v, findmaximumtree(updateboard, m, localdepth + 1, curentplayer, val))
            CallLogging(steps, localdepth, v)
        return v

def findmaximumtree(new_board, move, deep, p, val):
    if deep == depth:
        utility = evaluation_function(new_board, move, 3 - p)
        val -= utility
        CallLogging(move, deep, utility)
        return val
    else:
        v = sys.maxsize * -1
        value = evaluation_function(new_board, move, 3 - p)
        val -= value
        index = convert_alpha_to_index(move)
        new_board_with_m = setplayerandupdateboard(new_board, index[1], index[0], 3 - p)
        w = win(new_board, index[1], index[0], 3 - p)
        if w > 0:
            CallLogging(move, deep, val)
            return val
        new_moves = find_possible_moves_l(new_board_with_m, lines_matrix)
        new_moves = sorting_moves(new_moves)
        CallLogging(move, deep, NegativeInfinity)
        for m in new_moves:
            v = max(v, findminimumtree(new_board_with_m, m, deep + 1, p, val))
            CallLogging(move, deep, v)
        return v

def minimaxtreefind(mov):
    CallLogging("Move", "Depth", "Value")
    CallLogging("root", 0, NegativeInfinity)
    root_value = sys.maxsize * -1
    final_move = ""
    for m in mov:
        val = findminimumtree(currentBoardState, m, 1, num_player, 0)
        if val > root_value:
            root_value = val
            final_move = m
        CallLogging("root", 0, root_value)
    boardtofile(final_move, num_player)


def alphabetamin(currentboard, steps, localdeep, player, value, alpha, beta, maxPlayer):
    if localdeep == depth:
        value += evaluation_function(currentboard, steps, player)
        alphabetalogging(steps, localdeep, value, alpha, beta)
        return (value, alpha, beta)
    else:
        v = sys.maxsize
        value += evaluation_function(currentboard, steps, player)
        index = convert_alpha_to_index(steps)
        new_board_with_m = setplayerandupdateboard(currentboard, index[1], index[0], player)
        w = win(currentboard, index[1], index[0], player)
        if w > 0:
            alphabetalogging(steps, localdeep, value, alpha, beta)
            return (value, alpha, beta)
        new_moves = find_possible_moves_l(new_board_with_m, lines_matrix)
        new_moves = sorting_moves(new_moves)
        alphabetalogging(steps, localdeep, Infinity, alpha, beta)
        for m in new_moves:
            x, _, _ = alphabetamax(new_board_with_m, m, localdeep + 1, player, value, alpha, beta, maxPlayer)
            v = min(v, x)
            if player == maxPlayer:
                alpha = max(alpha, v)
            else:
                beta = min(beta, v)
            alphabetalogging(steps, localdeep, v, alpha, beta)
        return (v, alpha, beta)

def alphabetamax(new_board, move, d_max, p, val, alpha, beta, maxPlayer):
    if d_max == depth:
        val -= evaluation_function(new_board, move, 3 - p)
        alphabetalogging(move, d_max, val, alpha, beta)
        return (val, alpha, beta)
    else:
        v = sys.maxsize * -1
        value = evaluation_function(new_board, move, 3 - p)
        val -= value
        index = convert_alpha_to_index(move)
        new_board_with_m = setplayerandupdateboard(new_board, index[1], index[0], 3 - p)
        w = win(new_board, index[1], index[0], 3 - p)
        if w > 0:
            alphabetalogging(move, d_max, val, alpha, beta)
            return (val, alpha, beta)
        new_moves = find_possible_moves_l(new_board_with_m, lines_matrix)
        new_moves = sorting_moves(new_moves)
        alphabetalogging(move, d_max, NegativeInfinity, alpha, beta)
        for m in new_moves:
            y, _, _ = alphabetamin(new_board_with_m, m, d_max + 1, p, val, alpha, beta, maxPlayer)
            v = max(v, y)
            if p == maxPlayer:
                alpha = max(alpha, v)
            else:
                beta = min(beta, v)
            alphabetalogging(move, d_max, v, alpha, beta)
        return (v, alpha, beta)

def alphabetapruning(mov, alpha, beta, p, maxPlayer):
    alphabetalogging("Move", "Depth", "Value", "Alpha", "Beta")
    alphabetalogging("root", 0, NegativeInfinity, NegativeInfinity, Infinity)
    root_value = sys.maxsize * -1
    final_move = ""
    for m in mov:
        val, alpha, beta = alphabetamin(currentBoardState, m, 1, p, 0, alpha, beta, maxPlayer)
        if val > root_value:
            root_value = val
            final_move = m

            if p == maxPlayer:
                alpha = max(alpha, root_value)
            else:
                beta = min(beta, root_value)
        alphabetalogging("root", 0, root_value, alpha, beta)
        if beta <= alpha:
            break
    boardtofile(final_move, p)

def CallLogging(m, d, v):
    traverse_2_3.write("%s,%s,%s\n" % (m, d, v))

def alphabetalogging(m, d, v, alpha, beta):
    traverse_2_3.write("%s,%s,%s,%s,%s\n" % (m, d, v, alpha, beta))

pos_moves = find_possible_moves_l(currentBoardState, lines_matrix)
pos_moves = sorting_moves(pos_moves)

def alphafunc(maxPlayer):
    alpha = sys.maxsize * -1
    beta = sys.maxsize
    alphabetapruning(pos_moves, alpha, beta, num_player, maxPlayer)

def choose_algo():
    maxPlayer = num_player
    if task_type == 1:
        greedyfunctioncalling(currentBoardState, pos_moves)
    if task_type == 2:
        minimaxtreefind(pos_moves)
    if task_type == 3:
        alphafunc(maxPlayer)


choose_algo()

