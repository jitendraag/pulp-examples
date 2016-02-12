"""
The Looping Sudoku Problem Formulation for the PuLP Modeller

Authors: Antony Phillips, Dr Stuart Mitcehll
"""
# Import PuLP modeler functions
from pulp import *
from pprint import pprint

# A list of strings from "1" to "4" is created
Sequence = ["1", "2", "3", "4"]

# The Vals, Rows and Cols sequences all follow this form
Vals = Sequence
Rows = Sequence
Cols = Sequence

# The boxes list is created, with the row and column index of each square in each box
Boxes = [
         [('1', '1'), ('1', '2'), ('2', '1'), ('2', '2')],
         [('1', '3'), ('1', '4'), ('2', '3'), ('2', '4')],
         [('3', '1'), ('3', '2'), ('4', '1'), ('4', '2')],
         [('3', '3'), ('3', '4'), ('4', '3'), ('4', '4')]
        ]

pprint(Boxes)

Boxes =[]
for i in range(2):
    for j in range(2):
        Boxes += [[(Rows[2*i+k],Cols[2*j+l]) for k in range(2) for l in range(2)]]

# The prob variable is created to contain the problem data        
prob = LpProblem("Sudoku Problem",LpMinimize)

# The problem variables are created
choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)

# The arbitrary objective function is added
prob += 0, "Arbitrary Objective Function"

# A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

prob += lpSum([
            choices["1"]["1"]["1"],
            choices["2"]["1"]["1"],
            choices["3"]["1"]["1"],
            choices["4"]["1"]["1"],
        ]) == 1, ""

prob += lpSum([
            choices["1"]["1"]["2"],
            choices["2"]["1"]["2"],
            choices["3"]["1"]["2"],
            choices["4"]["1"]["2"],
        ]) == 1, ""

prob += lpSum([
            choices["1"]["1"]["3"],
            choices["2"]["1"]["3"],
            choices["3"]["1"]["3"],
            choices["4"]["1"]["3"],
        ]) == 1, ""

prob += lpSum([
            choices["1"]["1"]["4"],
            choices["2"]["1"]["4"],
            choices["3"]["1"]["4"],
            choices["4"]["1"]["4"],
        ]) == 1, ""


prob += lpSum([
            choices["1"]["2"]["1"],
            choices["2"]["2"]["1"],
            choices["3"]["2"]["1"],
            choices["4"]["2"]["1"],
        ]) == 1, ""

prob += lpSum([
            choices["1"]["2"]["2"],
            choices["2"]["2"]["2"],
            choices["3"]["2"]["2"],
            choices["4"]["2"]["2"],
        ]) == 1, ""


prob += lpSum([
            choices["1"]["2"]["3"],
            choices["2"]["2"]["3"],
            choices["3"]["2"]["3"],
            choices["4"]["2"]["3"],
        ]) == 1, ""

prob += lpSum([
            choices["1"]["2"]["4"],
            choices["2"]["2"]["4"],
            choices["3"]["2"]["4"],
            choices["4"]["2"]["4"],
        ]) == 1, ""


# The row, column and box constraints are added for each value
for v in Vals:
    for r in Rows:
        prob += lpSum([choices[v][r][c] for c in Cols]) == 1,""
        
    for c in Cols:
        prob += lpSum([choices[v][r][c] for r in Rows]) == 1,""

    #for b in Boxes:
    #    prob += lpSum([choices[v][r][c] for (r,c) in b]) == 1,""
                        
# The starting numbers are entered as constraints                
prob += choices["1"]["1"]["1"] == 1,""
prob += choices["2"]["2"]["1"] == 1,""

# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# A file called sudokuout.txt is created/overwritten for writing to
sudokuout = open('sudokuout.txt','w')

while True:
    prob.solve()
    # The status of the solution is printed to the screen
    print "Status:", LpStatus[prob.status]
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if LpStatus[prob.status] == "Optimal":
        # The solution is written to the sudokuout.txt file 
        for r in Rows:
            if r == "1" or r == "3":
                sudokuout.write("+-----+-----+\n")
            for c in Cols:
                for v in Vals:
                    if value(choices[v][r][c])==1:
                        if c == "1" or c == "3":
                            sudokuout.write("| ")
                        sudokuout.write(v + " ")
                        if c == "4":
                            sudokuout.write("|\n")
        sudokuout.write("+-----+-----+\n\n")
        # The constraint is added that the same solution cannot be returned again
        prob += lpSum([choices[v][r][c] for v in Vals
                                        for r in Rows
                                        for c in Cols
                                        if value(choices[v][r][c])==1]) <= 80
    # If a new optimal solution cannot be found, we end the program    
        break
    else:
        break
sudokuout.close()

# The location of the solutions is give to the user
print "Solutions Written to sudokuout.txt"

