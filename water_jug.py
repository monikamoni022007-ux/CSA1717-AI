jug4 = 0
jug3 = 0

while jug4 != 2 and jug3 != 2:

    if jug4 == 0:
        jug4 = 4
        print(jug4, jug3)

    elif jug3 == 3:
        jug3 = 0
        print(jug4, jug3)

    else:
        transfer = min(jug4, 3 - jug3)
        jug4 -= transfer
        jug3 += transfer
        print(jug4, jug3)

print("Goal Reached")