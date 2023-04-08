from copy import deepcopy
import matplotlib.pyplot as plt
import seaborn as sns

def ac3(csp, arcs_queue=None, current_domains=None, assignment=None):
    if arcs_queue is None:
        arcs_queue = create_arcs_queue(csp)
    else:
        arcs_queue = set(arcs_queue)

    if current_domains is None:
        current_domains = create_current_domains(csp)
    
    copied_current_domains = deepcopy(current_domains)

    while len(arcs_queue) > 0:
        Xi, Xj = arcs_queue.pop()
        copied_adjacency = deepcopy(csp.adjacency[Xi])
        
        if revise(csp, Xi, Xj, copied_current_domains):
            if len(copied_current_domains[Xi]) == 0:
                return False, copied_current_domains
            
            copied_adjacency.remove(Xj)

            for Xk in copied_adjacency:
                if Xk not in assignment.keys():
                    arcs_queue.add((Xk, Xi))
    
    return True, copied_current_domains

def revise(csp, Xi, Xj, current_domains):
    revised = False
    will_remove = []
    for x in current_domains[Xi]:
        consistent = False
        for y in current_domains[Xj]:
            if csp.constraint_consistent(Xi, x, Xj, y):
                consistent = True
    
        if not consistent:
            will_remove.append(x)
            revised = True

    for elm in will_remove:
        current_domains[Xi].remove(elm)
    
    return revised

def create_arcs_queue(csp):
    arcs_queue = set()
    for var1 in csp.adjacency:
        for var2 in csp.adjacency[var1]:
            arcs_queue.add((var1, var2))

    return arcs_queue

def create_current_domains(csp):
    return csp.domains

def backtracking(csp):
    return backtracking_helper(csp, {}, deepcopy(csp.domains))

def backtracking_helper(csp, assignment = {}, current_domains = None):
    if len(assignment.keys()) == len(csp.variables):
        return assignment
    
    unassigned_variables = []
    for elm in csp.variables:
        if elm not in assignment.keys():
            unassigned_variables.append(elm)
    
    var = select_unassigned_variable(unassigned_variables, current_domains)
    
    for value in current_domains[var]:
        if csp.check_partial_assignment(assignment):
            assignment[var] = value
            current_domains[var] = [value]

            unassigned_neighbors = []
            for neighbor in csp.adjacency[var]:
                if neighbor in unassigned_variables:
                    unassigned_neighbors.append(neighbor)

            arcs_queue = set()
            for neighbor in unassigned_neighbors:
                arcs_queue.add((var, neighbor))
                arcs_queue.add((neighbor, var))

            inferences_flag, inferences_domains = ac3(csp, arcs_queue, current_domains, assignment)
            if inferences_flag:
                result = backtracking_helper(csp, assignment, inferences_domains)
                if result is not None:
                    return result

            assignment.pop(var)
        
    return None

def select_unassigned_variable(unassigned_variables, current_domains):
    less_domains = float('inf')
    picked_variable = ''
    
    for d in current_domains:
        if d in unassigned_variables and len(current_domains[d]) < less_domains:
            less_domains = len(current_domains[d])
            picked_variable = d
    
    return picked_variable

class SudokuCSP:

    def __init__(self, partial_assignment={}):
        self.variables = []
        for row in range(1, 10):
            for col in range(1, 10):
                self.variables.append((row, col))

        self.domains = dict()
        for var in self.variables:
            if var in partial_assignment:
                self.domains[var] = [partial_assignment[var]]
            else:
                self.domains[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.adjacency = dict()

        for var in self.variables:
            self.adjacency[var] = []

        for var in self.variables:
            for i in range(1, 10):
                if i != var[1]:
                    self.adjacency[var].append((var[0], i))

            for i in range(1, 10):
                if i != var[0]:
                    self.adjacency[var].append((i, var[1]))

            row_start, row_end, col_start, col_end = 0, 0, 0, 0 #just initialization

            if var[0] <= 3:
                row_start, row_end = 1, 4
            elif var[0] <= 6:
                row_start, row_end = 4, 7
            else:
                row_start, row_end = 7, 10

            if var[1] <= 3:
                col_start, col_end = 1, 4
            elif var[1] <= 6:
                col_start, col_end = 4, 7
            else:
                col_start, col_end = 7, 10
                
            for i in range(row_start, row_end):
                for j in range(col_start, col_end):
                    if (i, j) not in self.adjacency[var] and (i, j) != var:
                        self.adjacency[var].append((i, j))
        
    def constraint_consistent(self, var1, val1, var2, val2):
        if var1 not in self.adjacency[var2]:
            return True
        
        if val1 != val2:
            return True
        
        return False
    
    def check_partial_assignment(self, assignment):
        if assignment is None:
            return False
        
        for elm in assignment:

            assigned_neighbors = []
            for adjacency in self.adjacency[elm]:
                if adjacency in assignment:
                    assigned_neighbors.append(adjacency)

            for adjacency in assigned_neighbors:
                if not self.constraint_consistent(elm, assignment[elm], adjacency, assignment[adjacency]):
                    return False
        
        return True
    
    def is_goal(self, assignment):
        if assignment is None:
            return False
        
        for var in self.variables:
            if var not in assignment:
                return False
            
        for elm in assignment:
            for adjacency in self.adjacency[elm]:
                if not self.constraint_consistent(elm, assignment[elm], adjacency, assignment[adjacency]):
                    return False
        
        return True
    
def visualize_sudoku_solution(assignment_solution, file_name):
    sudoku_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    for assignment in assignment_solution:
        sudoku_array[assignment[0] - 1][assignment[1] - 1] = assignment_solution[assignment]

    plt.figure(figsize=(9, 9))
    ax = sns.heatmap(data=sudoku_array, annot=True, linewidths=1.5, linecolor='k', cbar=False)
    ax.invert_yaxis()
    plt.savefig(file_name, format="png")
    plt.close()