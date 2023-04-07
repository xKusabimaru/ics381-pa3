from copy import deepcopy

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
