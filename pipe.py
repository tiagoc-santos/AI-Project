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

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    content = None
    size = 0
    
    def __init__(self, content, size):
        self.content = content
        self.size = size
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.content[row][col]

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

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        board = []
        line = stdin.readline().split()
        size = len(line)
        while line:
            board.append(line)  
            line = stdin.readline().split()
        return Board(np.array(board), size)
    
    def print(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if(j < (self.size - 1)):
                    print(self.get_value(i, j), end = '\t')
                else:
                    print(self.get_value(i, j))
    
    # TODO: outros metodos da classe
      
class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.state = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = np.array()
        for i in range(0, board.size):
            for j in range(0, self.size):
                actions = np.append(actions, (i, j, ))
        

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    problem = PipeMania(board)
    board.print()