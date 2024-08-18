from snake import Board, Direction


def test_game():
    board = Board(10, 10)

    print(board)
    board.tick()
    print(board)

    board.tick()
    print(board)


    board.tick()
    print(board)
    board.tick()
    print(board)
    board.tick(Direction.DOWN)
    print(board)
    board.tick()
    print(board)
    board.tick()
    print(board)
    board.tick()
    print(board)
