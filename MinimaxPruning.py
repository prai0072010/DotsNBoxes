import numpy as np

board_size = None
winning_score = None
total_node = 0

def mini_max(row_state, col_state, board_status, already_scored, depth):
    global board_size
    global winning_score
    global total_node
    global seen_state

    total_node = 0
    seen_state = []

    board_size = np.prod(board_status.shape)
    winning_score = round((board_size/2)) + 1
    
    ans = None
    max_move = -float('inf')

    alpha = -float('inf')
    beta = float('inf')
    
    player_turn = False
    axis = 'row'
    for r, c in successors(row_state):
        # print('Thinking at ',(axis, r, c))
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        if eval > max_move:
            max_move = eval
            ans = (axis, r, c)

        alpha = max(alpha, max_move)

        if alpha >= beta:
            break

    axis = 'col'
    for r, c in successors(col_state):
        # print('Thinking at ',(axis, r, c))
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        if eval > max_move:
            max_move = eval
            ans = (axis, r, c)

        alpha = max(alpha, max_move)

        if alpha >= beta:
            break
        
    print("node reached: ", total_node)
    return ans
    
def min_value(row_state, col_state, board_status, already_scored, is_score, alpha, beta, depth):
    global total_node
    total_node += 1
    player_turn = True

    if terminal(row_state, col_state, board_status) or depth == 0:
        return utility(board_status)
    
    min_eval = float('inf')
    axis = 'row'
    for r, c in successors(row_state):
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        min_eval = min(min_eval, eval)

        beta = min(beta, min_eval)

        if alpha >= beta:
            break

    axis = 'col'
    for r, c in successors(col_state):
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        min_eval = min(min_eval, eval)
        
        beta = min(beta, min_eval)

        if alpha >= beta:
            break

    return min_eval

def max_value(row_state, col_state, board_status, already_scored, is_score, alpha, beta, depth):
    global total_node
    total_node += 1

    player_turn = False

    if terminal(row_state, col_state, board_status) or depth == 0:
        return utility(board_status)

    max_eval = -float('inf')
    axis = 'row'
    for r, c in successors(row_state):
        move = row_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = min_value(move, col_state, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        max_eval = max(max_eval, eval)

        alpha = max(alpha, max_eval)

        if alpha >= beta:
            break

    axis = 'col'
    for r, c in successors(col_state):
        move = col_state.copy()
        move[r][c] = 1
        is_score, new_board_status, new_already_scored = scoring(axis, r, c, board_status.copy(), already_scored.copy(), player_turn)
        if is_score :
            eval = max_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)
        else:
            eval = min_value(row_state, move, new_board_status, new_already_scored, is_score, alpha, beta, depth-1)

        max_eval = max(max_eval, eval)

        alpha = max(alpha, max_eval)

        if alpha >= beta:
            break

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

def utility(board_status):
    ai_score = np.count_nonzero(board_status == 4) * 100
    player_score = np.count_nonzero(board_status == -4) * -100

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

