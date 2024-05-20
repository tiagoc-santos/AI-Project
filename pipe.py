# Grupo 06:
# 107301 João Ricardo Fernandes Caçador
# 106794 Tiago Castro Santos

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
from sys import stdin
from numpy import array

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

    

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    content = []
    size = 0
    assignments = np.array([])
    
    def __init__(self, content, size):
        self.content = content
        self.size = size
        self.domains = np.empty(size * size, dtype= object)
        self.is_valid = True
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.content[row][col]
    
    def board_index(self, row: int, col: int) -> int:
        """Devolve o indice de uma peca do tabulerio dada a sua linha e coluna."""
        return row * self.size + col

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if(row == 0):
            return (None, self.get_value(row+1, col))
        
        elif(row == (self.size - 1)):
            return (self.get_value(row-1, col), None)
        
        else:
            return(self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if(col == 0):
            return (None, self.get_value(row, col+1))
        
        elif(col == (self.size - 1)):
            return (self.get_value(row, col - 1), None)
        
        else:
            return(self.get_value(row, col-1), self.get_value(row, col+1))


    def create_domain(self, row: int, col: int, piece: str):
        if piece[0] == 'F':
            self.domains[self.board_index(row, col)] = np.array(['FC','FB','FE', 'FD'])
            
        elif piece[0] == 'B':
            self.domains[self.board_index(row, col)] = np.array(['BC', 'BB', 'BD', 'BE'])
        
        elif piece[0] == 'V':
            self.domains[self.board_index(row, col)] = np.array(['VC', 'VB','VD','VE'])
            
        elif piece[0] == 'L':
            self.domains[self.board_index(row, col)] = np.array(['LH', 'LV'])
        
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        line = stdin.readline().split()
        size = len(line)
        i = 0
        board = Board([], size)
        while line:
            board.content.append(line)  
            for j in range(0, size):
                board.create_domain(i, j, line[j])
                board.content[i][j] = board.domains[board.board_index(i, j)][0]
                if board.domains[board.board_index(i, j)].size == 1:
                    board.assignments = np.append(board.assignments, str(i) + str(j))
            i += 1
            line = stdin.readline().split()
        board.content = np.array(board.content)
        for row in range(0, size):
            for col in range(0, size):
                if row == 0:
                    board.satisfy_constraints_down(row, col)

                elif row == size - 1:
                    board.satisfy_constraints_up(row,col)
                
                if col == 0:
                    board.satisfy_constraints_right(row, col)
                
                elif col == size -1:
                    board.satisfy_constraints_left(row, col)
        return board
    
    def print(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if(j < (self.size - 1)):
                    print(self.get_value(i, j), end = '\t')
                else:
                    print(self.get_value(i, j))
    
    def satisfy_constraints_up(self, row: int, col:int):
        if row + 1 >= self.size:
            pipe1_domain = ['LH']
        else:
            pipe1_domain = self.domains[self.board_index(row+1, col)]
        
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]
        
        if pipe2[0] == 'F':
            restrictions = ['FC', 'FD', 'FE', 'FB']
        elif pipe2[0] == 'B':
            restrictions = ['BC', 'BD', 'BE', 'BB']
        elif pipe2[0] == 'V':
            restrictions = ['VC', 'VD', 'VE', 'VB']
        elif pipe2[0] == 'L':
            restrictions = ['LH', 'LV']

        for orientation in pipe1_domain:
            if orientation in ['FC', 'BC', 'BD', 'BE', 'VC', 'VD', 'LV']:
                if (pipe2[0] == 'F'):
                    if (orientation == 'FC'):
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FE', 'FB']]
                    else:    
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FE']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BC']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VD', 'VC']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LH']]
                
            else:
                if (pipe2[0] == 'F'):
                    restrictions = [item for item in restrictions if item in ['FB']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BB', 'BD', 'BE']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VB', 'VE']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LV']]

        new_domain = np.array([item for item in pipe2_domain if item not in restrictions])
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                self.assignments = []
                return False
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
            if not self.satisfy_constraints(row, col):
                return False
        return True

    def satisfy_constraints_down(self, row: int, col:int):
        if row - 1 < 0:
            pipe1_domain = ['LH']
        else:
            pipe1_domain = self.domains[self.board_index(row-1, col)]

        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]
        
        if pipe2[0] == 'F':
            restrictions = ['FC', 'FD', 'FE', 'FB']
        elif pipe2[0] == 'B':
            restrictions = ['BC', 'BD', 'BE', 'BB']
        elif pipe2[0] == 'V':
            restrictions = ['VC', 'VD', 'VE', 'VB']
        elif pipe2[0] == 'L':
            restrictions = ['LH', 'LV']
        
        for orientation in pipe1_domain:
            if orientation in ['FB', 'BD', 'BE', 'BB', 'VE', 'VB', 'LV']:
                if (pipe2[0] == 'F'):
                    if (orientation == 'FB'):
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FE', 'FB']]
                    else: 
                        restrictions = [item for item in restrictions if item in ['FB', 'FD', 'FE']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BB']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VE', 'VB']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LH']]
                
            else:
                if (pipe2[0] == 'F'):
                    restrictions = [item for item in restrictions if item in ['FC']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BC', 'BD', 'BE']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VC', 'VD']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LV']]

        new_domain = np.array([item for item in pipe2_domain if item not in restrictions])
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                self.assignments = []
                return False
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
            if not self.satisfy_constraints(row, col):
                return False
        return True

    def satisfy_constraints_left(self, row: int, col:int):
        if col + 1 >= self.size:
            pipe1_domain = ['LV']
        else:
            pipe1_domain = self.domains[self.board_index(row, col + 1)]
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]

        if pipe2[0] == 'F':
            restrictions = ['FC', 'FD', 'FE', 'FB']
        elif pipe2[0] == 'B':
            restrictions = ['BC', 'BD', 'BE', 'BB']
        elif pipe2[0] == 'V':
            restrictions = ['VC', 'VD', 'VE', 'VB']
        elif pipe2[0] == 'L':
            restrictions = ['LH', 'LV']
            
        for orientation in pipe1_domain:
            if orientation in ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']:
                if (pipe2[0] == 'F'):
                    if (orientation == 'FE'):
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FE', 'FB']]
                    else:    
                        restrictions = [item for item in restrictions if item in ['FC', 'FB', 'FE']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BE']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VE', 'VC']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LV']]
                
            else:
                if (pipe2[0] == 'F'):
                    restrictions = [item for item in restrictions if item in ['FD']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BB', 'BD', 'BC']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VB', 'VD']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LH']]

        new_domain = np.array([item for item in pipe2_domain if item not in restrictions])
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                self.assignments = []
                return False
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
            if not self.satisfy_constraints(row, col):
                return False
        return True
        
    def satisfy_constraints_right(self, row: int, col:int):
        if col - 1 < 0:
            pipe1_domain = ['LV']
        else:
            pipe1_domain = self.domains[self.board_index(row, col - 1)]
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]
        
        if pipe2[0] == 'F':
            restrictions = ['FC', 'FD', 'FE', 'FB']
        elif pipe2[0] == 'B':
            restrictions = ['BC', 'BD', 'BE', 'BB']
        elif pipe2[0] == 'V':
            restrictions = ['VC', 'VD', 'VE', 'VB']
        elif pipe2[0] == 'L':
            restrictions = ['LH', 'LV']

        for orientation in pipe1_domain:
            if orientation in ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']:
                if (pipe2[0] == 'F'):
                    if (orientation == 'FD'):
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FE', 'FB']]
                    else:    
                        restrictions = [item for item in restrictions if item in ['FC', 'FD', 'FB']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BD']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VB', 'VD']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LV']]
                
            else:
                if (pipe2[0] == 'F'):
                    restrictions = [item for item in restrictions if item in ['FE']]
                
                elif (pipe2[0] == 'B'):
                    restrictions = [item for item in restrictions if item in ['BB', 'BC', 'BE']]
                
                elif (pipe2[0] == 'V'):
                    restrictions = [item for item in restrictions if item in ['VC', 'VE']]

                elif (pipe2[0] == 'L'):
                    restrictions = [item for item in restrictions if item in ['LH']]

        new_domain = np.array([item for item in pipe2_domain if item not in restrictions])
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)
        
        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                self.assignments = []
                return False
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
            if not self.satisfy_constraints(row, col):
                return False
        return True
    
    def satisfy_constraints(self, row: int, col: int):
        size = self.size
        if row - 1 >= 0:
            if not self.satisfy_constraints_up(row-1, col):
                print("Dominio invalido")
                self.is_valid = False
                return False
                
        if col - 1 >= 0:
            if not self.satisfy_constraints_left(row, col-1):
                print("Dominio invalido")
                self.is_valid = False
                return False

        if row + 1 < size:
            if not self.satisfy_constraints_down(row+1, col):
                print("Dominio invalido")
                self.is_valid = False
                return False
                
        if col + 1 < size:
            if not self.satisfy_constraints_right(row, col+1):
                print("Dominio invalido")
                self.is_valid = False
                return False
        return True

    def create_new_board(self, action):
        new_board = Board(np.array([np.copy(inner_list) for inner_list in self.content]), self.size)
        new_board.content[action[0]][action[1]] = action[2]
        new_board.assignments = np.copy(self.assignments)
        new_board.assignments = np.append(new_board.assignments, str(action[0]) + str(action[1]))
        new_board.domains = np.copy(self.domains)
        new_board.domains[new_board.board_index(action[0], action[1])] = [action[2]]
        new_board.satisfy_constraints(action[0], action[1])
        return new_board
        
             
class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        if not board.is_valid:
            return []
        
        size = board.size
        actions = []
        
        for i in range(0, size):
            for j in range(0, size):
                for item in board.domains[board.board_index(i, j)]:
                    if ((item != board.get_value(i, j)) or (str(i) + str(j) not in board.assignments)):
                        actions.append((i, j, item))
        print(actions)
        return actions
        
        
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        print(action)
        return PipeManiaState(state.board.create_new_board(action))
       

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return len(state.board.assignments) == pow(state.board.size, 2)
           

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass


if __name__ == "__main__":
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    print(board.domains)
    board.print()
    problem = PipeMania(board)
    solution = depth_first_tree_search(problem)
    #solution.state.board.print()


