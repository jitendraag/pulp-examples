from pulp import *

# 0 <= x <= 3
x = LpVariable("x", 0, 3)

# 0 <= y <= 1
y = LpVariable("y", 0, 1)

prob = LpProblem("Just Starting", LpMinimize)

# Constraint x + y <= 2
prob += x + y <= 2

# Objective function -4*x + y
prob += -4*x + y
status = prob.solve()
prob.writeLP("simple.lp")
prob.solve()

if LpStatus[prob.status] == "Optimal":
    print "Optimal: x = {}, y = {}, objective function: {}".format(value(x), value(y), value(-4*x + y))
else:
    print LpStatus[prob.status]
