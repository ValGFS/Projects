import random

#Clase del juego
class TicTacToe ():
    def __init__(self, vs_cpu=False, cpu_symbol='O' ):
        self.board = [''] * 9   #Crear el tablero
        self.current_player = 'X'
        self.vs_cpu = vs_cpu
        self.cpu_symbol = cpu_symbol

    #Mostrar el tablero
    def show_board (self):
        def c(i):
            return self.board[i] if self.board[i] else ' '

        print('\n     Tic Tac Toe\n')
        row = '    {:^3}|{:^3}|{:^3}   ({} | {} | {})'
        sep = '    ---+---+---'
        print (row.format(c(0), c(1), c(2), 1, 2, 3))
        print (sep)
        print (row.format(c(3), c(4), c(5), 4, 5, 6))
        print(sep)
        print (row.format(c(6), c(7), c(8), 7, 8, 9))

    #Validación de movimiento
    def valid_move (self, position):
        index = position - 1
        return 1 <= position <= 9 and self.board[index] == ''

    #Validar el movimiento del jugador
    def player_move (self, position):
        index = position - 1
        self.board[index] = self.current_player

    def cpu_move (self):
        print (f'\n Turno de tu tio {self.cpu_symbol}')
        empty_positions = [i + 1 for i, value in enumerate(self.board) if value == '']
        position = random.choice(empty_positions)
        self.player_move(position)

    #Función para definir el ganador
    def winner (self):
        winning_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), #Combinaciones de lineas
            (0, 3, 6), (1, 4, 7), (2, 5, 8), #Combinación de columnas
            (0, 4, 8), (2, 4 ,6)             #Combinación en diagonal
        ]
        return any (self.board[a] == self.board[b] == self.board[c] == self.current_player for a, b, c in winning_lines)

    #Definicón de un empate
    def draw (self):
        return '' not in self.board

    #Cambio de jugador
    def switch_player (self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    #Función principal para correr el juego
    def play (self):
        self.board = [''] * 9
        self.current_player ='X'
        self.show_board()

        while True:
            if self.vs_cpu and self.current_player == self.cpu_symbol:
                self.cpu_move()
            else:
                try:
                    player_input = input (f'\nJugador {self.current_player}, elige una posicion del 1 al 9:').strip()
                    position = int(player_input)
                except ValueError:
                    print (f'Posicion no valida, escribe un numero del 1  al 9')
                    continue

                if not self.valid_move(position):
                    print ('\nMovimiento invalido. Vuelve a intentar')
                    continue

                self.player_move (position)
            self.show_board ()

            if self.winner ():
                print (f'\nFelicidades jugador {self.current_player} has ganado!')
                break

            if self.draw ():
                print ('\nEmpate.\nNo hay mas movimientos. Juego finalizado.')
                break

            self.switch_player()

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
        print ('1. Partida entre 2 jugadores')
        print ('2. Jugar contra CPU')
        print ('3. Instrucciones')
        print ('4. Salir')

        option = input ('\nSeleccione una opcion: ')
        if option == '1':
            game = TicTacToe()
            game.play()
        elif option == '2':
            choice = input ('\n¿Escoge tu simbolo X o O?: ').strip().upper()
            player_symbol = choice if choice in ['X', 'O'] else 'X'
            cpu_symbol = 'O' if player_symbol == 'X' else 'X'
            game = TicTacToe(vs_cpu=True, cpu_symbol=cpu_symbol)
            game.current_player = 'X'
            game.play()

        elif option == '3':
            instructions()
        elif option == '4':
            print ('\nSaliendo del juego. ¡Hasta luego!')
            break
        else:
            print ('\nOpcion no valida, Intenta nuevamente')
            continue

game_menu()