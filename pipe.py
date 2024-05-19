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
        if row == 0:
            if piece[0] == 'F':
                if col == 0:
                    self.domains[self.board_index(row, col)] = np.array(['FB', 'FD'])
                elif col == self.size -1:
                    self.domains[self.board_index(row, col)] = np.array(['FB', 'FE'])
                else:
                    self.domains[self.board_index(row, col)] = np.array(['FB', 'FE', 'FD'])
            
            elif piece[0] == 'B':
                self.domains[self.board_index(row, col)] = np.array(['BB'])
            
            elif piece[0] == 'V':
                if col == 0:
                    self.domains[self.board_index(row, col)] = np.array(['VB'])
                elif col == self.size -1:
                    self.domains[self.board_index(row, col)] = np.array(['VE']) 
                else:
                    self.domains[self.board_index(row, col)] = np.array(['VB', 'VE'])
            elif piece[0] == 'L':
                self.domains[self.board_index(row, col)] = np.array(['LH'])

        elif row == self.size - 1:
            if piece[0] == 'F':
                if col == 0:
                    self.domains[self.board_index(row, col)] = np.array(['FC', 'FD'])
                elif col == self.size -1:
                    self.domains[self.board_index(row, col)] = np.array(['FC', 'FE'])
                else:
                    self.domains[self.board_index(row, col)] = np.array(['FC', 'FE', 'FD'])
            
            elif piece[0] == 'B':
                self.domains[self.board_index(row, col)] = np.array(['BC'])
            
            elif piece[0] == 'V':
                if col == 0:
                    self.domains[self.board_index(row, col)] = np.array(['VD'])
                elif col == self.size -1:
                    self.domains[self.board_index(row, col)] = np.array(['VC']) 
                else:
                    self.domains[self.board_index(row, col)] = np.array(['VD', 'VC'])         
            else:
                self.domains[self.board_index(row, col)] = np.array(['LH'])
        
        elif col == 0:
            if piece[0] == 'F':
                self.domains[self.board_index(row, col)] = np.array(['FC','FB','FD'])
                
            elif piece[0] == 'B':
                self.domains[self.board_index(row, col)] = np.array(['BD'])
            
            elif piece[0] == 'V':
                self.domains[self.board_index(row, col)] = np.array(['VD', 'VB'])
            
            else:
                self.domains[self.board_index(row, col)] = np.array(['LV'])
        
        elif col == self.size -1:
            if piece[0] == 'F':
                self.domains[self.board_index(row, col)] = np.array(['FC','FB','FE'])
                
            elif piece[0] == 'B':
                self.domains[self.board_index(row, col)] = np.array(['BE'])
            
            elif piece[0] == 'V':
                self.domains[self.board_index(row, col)] = np.array(['VC', 'VE'])
                
            else:
                self.domains[self.board_index(row, col)] = np.array(['LV'])
        else:
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
        return board
    
    def print(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if(j < (self.size - 1)):
                    print(self.get_value(i, j), end = '\t')
                else:
                    print(self.get_value(i, j))
    
    def satisfy_constraints_up(self, row: int, col:int):
        pipe1 = self.get_value(row + 1, col)
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]

        if pipe1 in ['FC', 'BC', 'BD', 'BE', 'VC', 'VD', 'LV']:
            if (pipe2[0] == 'F'):
                if (pipe1 == 'FC'):
                    restrictions = np.array(['FC', 'FD', 'FE', 'FB'])
                else:    
                    restrictions = np.array(['FC', 'FD', 'FE'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BC'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VD', 'VC'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LH'])
            
        else:
            if (pipe2[0] == 'F'):
                restrictions = np.array(['FB'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BB', 'BD', 'BE'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VB', 'VE'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LV'])

        new_domain = [item for item in pipe2_domain if item not in restrictions]
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                print("Dominio vazio")
                self.assignments = []
                return False
            print("-------------------")
            print("mudou em cima de " + str(row+1) + str(col))
            self.print()
            print(self.domains)
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
                print(self.assignments)
            print("-------------------")
            if not self.satisfy_constraints(row, col):
                return False
        return True

    def satisfy_constraints_down(self, row: int, col:int):
        pipe1 = self.get_value(row - 1, col)
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]
        
        if pipe1 in ['FB', 'BD', 'BE', 'BB', 'VE', 'VB', 'LV']:
            if (pipe2[0] == 'F'):
                if (pipe1 == 'FB'):
                    restrictions = np.array(['FC', 'FD', 'FE', 'FB'])
                else: 
                    restrictions = np.array(['FB', 'FD', 'FE'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BB'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VE', 'VB'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LH'])
            
        else:
            if (pipe2[0] == 'F'):
                restrictions = np.array(['FC'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BC', 'BD', 'BE'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VC', 'VD'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LV'])

        new_domain = [item for item in pipe2_domain if item not in restrictions]
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                print("Dominio vazio")
                self.assignments = []
                return False
            print("-------------------")
            print("mudou em baixo de " + str(row-1) + str(col))
            self.print()
            print(self.domains)
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
                print(self.assignments)
            print("-------------------")
            if not self.satisfy_constraints(row, col):
                return False
        return True

    def satisfy_constraints_left(self, row: int, col:int):
        pipe1 = self.get_value(row, col + 1)
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]

        if pipe1 in ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']:
            if (pipe2[0] == 'F'):
                if (pipe1 == 'FE'):
                    restrictions = np.array(['FC', 'FD', 'FE', 'FB'])
                else:    
                    restrictions = np.array(['FC', 'FB', 'FE'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BE'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VE', 'VC'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LV'])
            
        else:
            if (pipe2[0] == 'F'):
                restrictions = np.array(['FD'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BB', 'BD', 'BC'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VB', 'VD'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LH'])

        new_domain = [item for item in pipe2_domain if item not in restrictions]
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)

        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                print("Dominio vazio")
                self.assignments = []
                return False
            print("-------------------")
            print("mudou a esquerda de " + str(row) + str(col+1))
            self.print()
            print(self.domains)
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
                print(self.assignments)
            print("-------------------")
            if not self.satisfy_constraints(row, col):
                return False
        return True
        
    def satisfy_constraints_right(self, row: int, col:int):
        pipe1 = self.get_value(row, col - 1)
        pipe2 = self.get_value(row, col)
        pipe2_domain = self.domains[self.board_index(row, col)]

        if pipe1 in ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']:
            if (pipe2[0] == 'F'):
                if (pipe1 == 'FD'):
                    restrictions = np.array(['FC', 'FD', 'FE', 'FB'])
                else:    
                    restrictions = np.array(['FC', 'FD', 'FB'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BD'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VB', 'VD'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LV'])
            
        else:
            if (pipe2[0] == 'F'):
                restrictions = np.array(['FE'])
            
            elif (pipe2[0] == 'B'):
                restrictions = np.array(['BB', 'BC', 'BE'])
            
            elif (pipe2[0] == 'V'):
                restrictions = np.array(['VC', 'VE'])

            elif (pipe2[0] == 'L'):
                restrictions = np.array(['LH'])

        new_domain = [item for item in pipe2_domain if item not in restrictions]
        self.domains[self.board_index(row, col)] = new_domain
        new_domain_size = len(new_domain)
        
        if len(pipe2_domain) > new_domain_size:
            if new_domain_size == 0:
                print("Dominio vazio")
                self.assignments = []
                return False
            print("-------------------")
            print("mudou a direita de " + str(row) + str(col-1))
            self.print()
            print(self.domains)
            self.content[row][col] = new_domain[0]
            if new_domain_size == 1 and (str(row) + str(col) not in self.assignments):
                self.assignments = np.append(self.assignments, str(row) + str(col))
                print(self.assignments)
            print("-------------------")
            if not self.satisfy_constraints(row, col):
                return False
        return True
    
    def satisfy_constraints(self, row: int, col: int):
        size = self.size
        if row - 1 >= 0:
            if not self.satisfy_constraints_up(row-1, col):
                self.is_valid = False
                return False
                
        if col - 1 >= 0:
            if not self.satisfy_constraints_left(row, col-1):
                self.is_valid = False
                return False

        if row + 1 < size:
            if not self.satisfy_constraints_down(row+1, col):
                self.is_valid = False
                return False
                
        if col + 1 < size:
            if not self.satisfy_constraints_right(row, col+1):
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
            print("oops")
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
    problem = PipeMania(board)
    solution = depth_first_tree_search(problem)
    solution.state.board.print()


