import numpy as np

board_size = None
winning_score = None

def mini_max(row_state, col_state, board_status, already_scored, depth):
    global board_size
    global winning_score

    board_size = np.prod(board_status.shape)
    winning_score = round((board_size/2)) + 1
    
    ans = None
    max_move = -float('inf')

    player_turn = False
    axis = 'row'
    for r, c in successors(row_state):
        # print('Thinking at ',(axis, r, c))
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)

        if eval > max_move:
            max_move = eval
            ans = (axis, r, c)

    axis = 'col'
    for r, c in successors(col_state):
        # print('Thinking at ',(axis, r, c))
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)

        if eval > max_move:
            max_move = eval
            ans = (axis, r, c)
        
    return ans
    
def min_value(row_state, col_state, board_status, already_scored, is_score, depth):
    player_turn = True

    if terminal(row_state, col_state, board_status) or depth == 0:
        return utility(board_status, player_turn, is_score)
    
    min_eval = float('inf')
    axis = 'row'
    for r, c in successors(row_state):
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)

        min_eval = min(min_eval, eval)

    axis = 'col'
    for r, c in successors(col_state):
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)

        min_eval = min(min_eval, eval)

    return min_eval

def max_value(row_state, col_state, board_status, already_scored, is_score, depth):
    player_turn = False

    if terminal(row_state, col_state, board_status) or depth == 0:
        return utility(board_status, player_turn, is_score)

    max_eval = -float('inf')
    axis = 'row'
    for r, c in successors(row_state):
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, depth-1)

        max_eval = max(max_eval, eval)

    axis = 'col'
    for r, c in successors(col_state):
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)
        else:
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, depth-1)

        max_eval = max(max_eval, eval)

    return max_eval

def successors(state):
    moves = []
    for r in range(state.shape[0]):
        for c in range(state.shape[1]):
            if state[r][c] != 1:
                moves.append((r, c))
    return moves

def terminal(row_state, col_state, board_status):
    board_full = ((row_state == 1).all() and (col_state == 1).all()) 
    com_winning = np.count_nonzero(board_status == 4) >= winning_score
    player_winning = np.count_nonzero(board_status == -4) >= winning_score
    return board_full or com_winning or player_winning

def utility(board_status, player_turn, is_score):
    ai_score = np.count_nonzero(board_status == 4) * 100
    player_score = np.count_nonzero(board_status == -4) * -100

    # extra_score = 0
    # lose_score = 0
    # if not player_turn:
    #     if is_score:
    #         extra_score = np.count_nonzero(board_status == 3) * 1
    #     else:
    #         lose_score = np.count_nonzero(board_status == 3) * -1
    # else:
    #     if is_score:
    #         extra_score = np.count_nonzero(board_status == 3) * -1
    #     else:
    #         lose_score = np.count_nonzero(board_status == 3) * 1

    game_score = ai_score + player_score

    if np.count_nonzero(board_status < -4) > 0 or np.count_nonzero(board_status > 4) > 0 :
        print(board_status)

    return game_score

def scoring(axis, r, c, board_status, already_scored, player_turn):
    is_score = False
    if r < (board_status.shape[0]) and c < (board_status.shape[1]):
        board_status[r][c] += 1

    if axis == 'row':
        if r >= 1:
            board_status[r-1][c] += 1

    elif axis == 'col':
        if c >= 1:
            board_status[r][c-1] += 1

    boxes = np.argwhere(board_status == 4)
    for box in boxes:
        if list(box) not in already_scored and list(box) !=[]:
            already_scored.append(list(box))
            score_row, score_col = box
            if player_turn:
                board_status[score_row][score_col] = -4
            is_score = True

    return is_score, board_status, already_scored

# def is_seen_state(row_state, col_state, board_status, player_turn):
#     global seen_state
#     if (tuple(row_state.flatten()), tuple(col_state.flatten()), tuple(board_status.flatten()), player_turn) not in seen_state:
#         seen_state.append((tuple(row_state.flatten()), tuple(col_state.flatten()), tuple(board_status.flatten()), player_turn))
#         return False
#     else:
#         return True
