import sys

# python main.py inputs/ex1.var.txt inputs/ex1.con.txt none
# python main.py inputs/ex2.var.txt inputs/ex2.con.txt none
# python main.py inputs/ex3.var.txt inputs/ex3.con.txt none

'''
DATA STRUCTURES

unassigned_vars: ['A','B','F']

assigned_vars: {'A':3, 'B': 2}

domains:
{'A': [1, 2, 3, 4, 5],
 'B': [1, 2, 3, 4, 5],
 'C': [1, 2, 3, 4, 5],
 'D': [1, 2, 3, 4, 5],
 'E': [1, 2, 3],
 'F': [1, 2]}

constraints:
{'A': {'B': '>', 'C': '>', 'D': '>'},
 'B': {'A': '<', 'F': '>'},
 'C': {'A': '<', 'E': '>'},
 'D': {'A': '<', 'E': '='},
 'E': {'C': '<', 'D': '='},
 'F': {'B': '<'}}
 e.g., first line encodes A > B, A > C, A > D

'''

def read_domains(var_filename):
    f = open(var_filename, "r")
    lines = [line.rstrip() for line in f.readlines()]
    domains = {}
    for line in lines:
        var, vals = tuple(line.split(": "))
        domains[var] = [int(val) for val in vals.split(" ")]
    return domains

def reverse_op(op):
  if op == "=":
    return "="
  elif op == "!":
    return "!"
  elif op == ">":
    return "<"
  elif op == "<":
    return ">"
  else:
    return None
  
def read_constraints(con_filename, domains):
    constraints = {var:{} for var in domains.keys()}

    f = open(con_filename, "r")
    lines = [line.rstrip() for line in f.readlines()]
    for line in lines:
        var1, op, var2 = tuple(line.split(" "))
        constraints[var1][var2] = op
        constraints[var2][var1] = reverse_op(op)
    return constraints

def evaluate(val1, val2, op):
  if op == "=":
    return val1 == val2
  elif op == "!":
    return not val1 == val2
  elif op == ">":
    return val1 > val2
  elif op == "<":
    return val1 < val2
  else:
    return None

def check_constraints(var1, val1, assigned_vars, constraints):
  constraints_for_var = constraints[var1]
  assigned_vars = dict([t for t in assigned_vars.items() if t[0] in constraints_for_var.keys()])
  for var2, val2 in assigned_vars.items():
    if not evaluate(val1, val2, constraints_for_var[var2]):
      return False
  return True

def legal_values(var, assigned_vars, domains, constraints):
  return [val for val in domains[var] if check_constraints(var, val, assigned_vars, constraints)]

def remaining_constraints(var, unassigned_vars, constraints):
  return [t for t in constraints[var].items() if t[0] in unassigned_vars]

def next_var(assigned_vars, domains, constraints):
  unassigned_vars = [v for v in domains.keys() if v not in assigned_vars.keys()]
  if len(unassigned_vars) == 0:
    return None
  unassigned_vars.sort()
  unassigned_vars.sort(key = lambda x: len(remaining_constraints(x, unassigned_vars, constraints)), reverse=True)
  unassigned_vars.sort(key = lambda x: len(legal_values(x, assigned_vars, domains, constraints)))
  return unassigned_vars[0]

def next_val(var, assigned_vars, domains, constraints):

    unassigned_vars = [v for v in domains.keys() if v not in assigned_vars.keys()]
    counts = {}
    unassigned_vars = remove(unassigned_vars, var)

    for val in domains[var]:
      num_legal_vals = 0
      assigned_vars[var] = val
      #print(val)
      for uv in unassigned_vars:
        #print(uv, legal_values(uv, assigned_vars, domains, constraints))
        num_legal_vals += len(legal_values(uv, assigned_vars, domains, constraints))
      #print()
      counts[val] = num_legal_vals


    counts = list(counts.items())
    counts.sort(key = lambda x: x[0])
    counts.sort(key = lambda x: x[1], reverse=True)
    return [count[0] for count in counts]

def remove(l, item):
  return [i for i in l if i != item]

def dict_remove(d, key):
  return {t[0]:t[1] for t in d.items() if not t[0] == key}

def dict_add(d, key, value):
  return {**d, **{key:value}}

def DFS(assignment, domains, constraints):
  print()
  print(assignment)

  # if no more variables left,
  unassigned = sorted(list(set(domains.keys()) - set(assignment.keys())))
  if not unassigned:
    return True

  # choose variable to assign
  var = next_var(assignment, domains, constraints)
  print("choosing", var, "next")

  # for each value of this variable
  for val in next_val(var, assignment, domains, constraints):
    # check if it satisfies all the constraints and if it does, proceed.
    # if not, then check the next value
    if check_constraints(var, val, assignment, constraints):
      print(var, "=", val, "works for now")
      if DFS(dict_add(assignment, var, val), domains, constraints):
        return True
    else:
      print(var, "=", val, "does not work")
  # if none of the values work then we made a mistake before, so return
  print("Nothing works for", var, "so going back up")
  return False

def main(var_filename, con_filename, procedure):
    domains = read_domains(var_filename)
    constraints = read_constraints(con_filename, domains)
    DFS({}, domains, constraints)

if __name__ == "__main__":
    var_file = sys.argv[1]
    con_file = sys.argv[2]
    procedure = sys.argv[3]
    main(var_file, con_file, procedure)