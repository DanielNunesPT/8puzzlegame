# Representa o tabuleiro do 8-puzzle
class Puzzle:
    def __init__(self, state):
        self.state = state
        self.size = int(len(state) ** 0.5)  # Determina o tamanho do tabuleiro (3x3, por exemplo)
        self.zero_position = self.state.index(0)  # Encontra a posição do espaço vazio

    def is_goal(self, goal_state):
        # Verifica se o estado atual é o objetivo
        return self.state == goal_state

    def get_neighbors(self):
        # Retorna uma lista de vizinhos possíveis (novos estados após mover o espaço vazio)
        neighbors = []
        zero_row = self.zero_position // self.size
        zero_col = self.zero_position % self.size
        
        # Definir possíveis movimentos para o espaço vazio
        moves = [
            ("up", zero_row > 0),  # Mover para cima
            ("down", zero_row < self.size - 1),  # Mover para baixo
            ("left", zero_col > 0),  # Mover para a esquerda
            ("right", zero_col < self.size - 1)  # Mover para a direita
        ]
        
        for move, condition in moves:
            if condition:
                new_zero_position = self.zero_position
                if move == "up":
                    new_zero_position -= self.size
                elif move == "down":
                    new_zero_position += self.size
                elif move == "left":
                    new_zero_position -= 1
                elif move == "right":
                    new_zero_position += 1
                
                # Troca o espaço vazio com a posição desejada
                new_state = list(self.state)
                new_state[self.zero_position], new_state[new_zero_position] = new_state[new_zero_position], new_state[self.zero_position]
                
                # Adiciona o novo estado à lista de vizinhos
                neighbors.append(Puzzle(new_state))
        
        return neighbors

# Busca em Largura (BFS)
def bfs(initial_state, goal_state):
    initial_puzzle = Puzzle(initial_state)
    queue = [initial_puzzle]
    visited = set()
    parent_map = {tuple(initial_puzzle.state): None}  # Map para rastrear pais de cada estado
    
    while queue:
        current_puzzle = queue.pop(0)  # Remove o primeiro elemento da lista
        
        if current_puzzle.is_goal(goal_state):
            # Caminho para a solução encontrado, constrói a sequência de movimentos
            return reconstruct_path(parent_map, current_puzzle, initial_puzzle)
        
        # Adiciona estado atual aos visitados
        visited.add(tuple(current_puzzle.state))
        
        for neighbor in current_puzzle.get_neighbors():
            if tuple(neighbor.state) not in visited:
                # Adiciona o vizinho à fila
                queue.append(neighbor)
                
                # Mapeia o vizinho para o estado atual como seu pai
                parent_map[tuple(neighbor.state)] = current_puzzle
    
    return None

# Busca em Profundidade (DFS)
def dfs(initial_state, goal_state):
    initial_puzzle = Puzzle(initial_state)
    stack = [initial_puzzle]
    visited = set()
    parent_map = {tuple(initial_puzzle.state): None}  # Map para rastrear pais de cada estado
    
    while stack:
        current_puzzle = stack.pop()  # Remove o último elemento da lista
        
        if current_puzzle.is_goal(goal_state):
            # Caminho para a solução encontrado, constrói a sequência de movimentos
            return reconstruct_path(parent_map, current_puzzle, initial_puzzle)
        
        # Adiciona estado atual aos visitados
        visited.add(tuple(current_puzzle.state))
        
        for neighbor in current_puzzle.get_neighbors():
            if tuple(neighbor.state) not in visited:
                # Adiciona o vizinho à pilha
                stack.append(neighbor)
                
                # Mapeia o vizinho para o estado atual como seu pai
                parent_map[tuple(neighbor.state)] = current_puzzle
    
    return None

# Função para reconstruir o caminho a partir de um mapa de pais
def reconstruct_path(parent_map, goal_puzzle, initial_puzzle):
    path = []
    current_puzzle = goal_puzzle
    
    while current_puzzle != initial_puzzle:
        path.append(current_puzzle)
        current_puzzle = parent_map[tuple(current_puzzle.state)]
    
    # Inverte o caminho para mostrar na ordem correta
    path.reverse()
    return path

# Implementação das heurísticas

# Distância de Manhattan
def manhattan_distance(puzzle, goal_state):
    total_distance = 0
    size = puzzle.size
    
    for i, value in enumerate(puzzle.state):
        if value != 0:
            goal_index = goal_state.index(value)
            current_row, current_col = i // size, i % size
            goal_row, goal_col = goal_index // size, goal_index % size
            total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    
    return total_distance

# Distância de Hamming
def hamming_distance(puzzle, goal_state):
    return sum(1 for i in range(len(puzzle.state)) if puzzle.state[i] != goal_state[i] and puzzle.state[i] != 0)

# Busca Best First (Greedy) com base em heurísticas
def greedy_best_first(initial_state, goal_state, heuristic):
    initial_puzzle = Puzzle(initial_state)
    frontier = [(0, initial_puzzle)]
    visited = set()
    parent_map = {tuple(initial_puzzle.state): None}
    
    while frontier:
        # Ordena a lista de fronteira com base no custo heurístico
        frontier.sort(key=lambda x: x[0])
        current_puzzle = frontier.pop(0)[1]  # Remove o estado com menor custo
        
        if current_puzzle.is_goal(goal_state):
            # Caminho para a solução encontrado, constrói a sequência de movimentos
            return reconstruct_path(parent_map, current_puzzle, initial_puzzle)
        
        # Adiciona estado atual aos visitados
        visited.add(tuple(current_puzzle.state))
        
        for neighbor in current_puzzle.get_neighbors():
            if tuple(neighbor.state) not in visited:
                heuristic_cost = heuristic(neighbor, goal_state)
                
                # Adiciona o vizinho à lista de fronteira
                frontier.append((heuristic_cost, neighbor))
                
                # Mapeia o vizinho para o estado atual como seu pai
                parent_map[tuple(neighbor.state)] = current_puzzle
    
    return None

# Função principal
def main():
    # Solicitação dos estados inicial e objetivo
    initial_state = input("Insira o estado inicial (9 números separados por espaços): ").split()
    initial_state = [int(num) for num in initial_state]
    
    goal_state = input("Insira o estado objetivo (9 números separados por espaços): ").split()
    goal_state = [int(num) for num in goal_state]
    
    # Escolha do algoritmo de busca
    algorithm = input("Escolha o algoritmo de busca (bfs, dfs, greedy): ")
    
    # Escolha da heurística (apenas para o algoritmo greedy)
    heuristic = None
    if algorithm == 'greedy':
        heuristic_choice = input("Escolha a heurística (manhattan, hamming): ")
        if heuristic_choice == 'manhattan':
            heuristic = manhattan_distance
        elif heuristic_choice == 'hamming':
            heuristic = hamming_distance
        else:
            print("Heurística não reconhecida.")
            return
    
    # Execução do algoritmo de busca escolhido
    if algorithm == 'bfs':
        path = bfs(initial_state, goal_state)
    elif algorithm == 'dfs':
        path = dfs(initial_state, goal_state)
    elif algorithm == 'greedy':
        path = greedy_best_first(initial_state, goal_state, heuristic)
    else:
        print("Algoritmo não reconhecido.")
        return
    
    # Exibir o resultado
    if path:
        print("Solução:")
        for puzzle in path:
            print(puzzle.state)
    else:
        print("Não foi encontrada uma solução.")

if __name__ == "__main__":
    main()
