#Crear el tablero
def create_board ():
    return [''] * 9

#Mostrar el tablero
def show_board (board):
    def c(i):
        return board[i] if board[i] else ' '

    print('\n     Tic Tac Toe\n')
    row = '    {:^3}|{:^3}|{:^3}   ({} | {} | {})'
    sep = '    ---+---+---'
    print (row.format(c(0), c(1), c(2), 1, 2, 3))
    print (sep)
    print (row.format(c(3), c(4), c(5), 4, 5, 6))
    print(sep)
    print (row.format(c(6), c(7), c(8), 7, 8, 9))

#Validación de movimiento
def valid_move (board, position):
    index = position - 1
    return 1 <= position <= 9 and board[index] == ''

#Validar el movimiento del jugador
def player_move (board, position, player):
    index = position - 1
    board[index] = player

#Función para definir el ganador
def winner (board, player):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), #Combinaciones de lineas
        (0, 3, 6), (1, 4, 7), (2, 5, 8), #Combinación de columnas
        (0, 4, 8), (2, 4 ,6)             #Combinación en diagonal
    ]
    return any (board[a] == board[b] == board[c] == player for a, b, c in winning_lines)

#Definicón de un empate
def draw (board):
    return '' not in board

#Cambio de jugador
def switch_player (player):
    return 'O' if player == 'X' else 'X'

#Función principal para correr el juego
def play ():
    board = create_board()
    current_player ='X'
    show_board(board)

    while True:
        try:
            player_input = input (f'\nJugador {current_player}, elige una posicion del 1 al 9:').strip()
            position = int(player_input)
        except ValueError:
            print (f'Posicion no valida, escribe un numero del 1  al 9')
            continue

        if not valid_move(board, position):
            print ('\nMovimiento invalido. Vuelve a intentar')
            continue

        player_move (board, position, current_player)
        show_board (board)

        if winner (board, current_player):
            print (f'\nFelicidades jugador {current_player} has ganado!')
            break

        if draw (board):
            print (f'\nEmpate.\nNo hay mas movimientos. Juego finalizado.')
            break

        current_player = switch_player (current_player)

def instructions ():
    print('Bievenido a Tic Tac Toe.\n')
    print('Las reglas son las siguientes:\n')
    print('1. Hay dos jugadores en cada partida. Uno utiliza la "X" y el otro usa la "O" como representacion para cada uno.')
    print('2. Selecciona un numero del 1 al 9, esto corresponde a la ubicacion donde se realizara tu jugada.')
    print('3. Si la posicion ya esta ocupada, no es posible volver a seleccionarlo.')
    print('4. Para poder ganar se debe realizar una linea vertical, horizontal o diagonal con un solo simbolo, ya sea con la "X" o la "O".')
    print('5. Si por alguna razon, se agotan los movimientos, el juego acabar en un empate.')

def game_menu():
    while True:
        print ('\n---Tic Tac Toe---\nSeleccione una opcion\n')
        print ('1. Nueva Partida')
        print ('2. Instrucciones')
        print ('3. Salir')

        option = input ('\nSeleccione una opcion: ')
        if option == '1':
            play()
        elif option == '2':
            instructions()
        elif option == '3':
            print ('\nSaliendo del juego. ¡Hasta luego!')
            break
        else:
            print ('\nOpcion no valida, Intenta nuevamente')
            continue