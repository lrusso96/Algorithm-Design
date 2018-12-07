class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # simple distance function in {0,1,3}
    def dist_to(self, point):
        if self.x == point.x and self.y == point.y:
            return 0
        if self.x == point.x or self.y == point.y:
            return 1
        return 3

    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + " )"

def ex1(X):
    C = []
    N = X.copy()
    dist_from_C = {}

    for point in N:
        dist_from_C[point] = 3 #max d!
    max_d = []
        
    picked = N[0]
    
    while len(N) > 0:
        N.remove(picked)
        C.append(picked)

        max_d.append(-1)

        for point in N:
            if picked.dist_to(point) < dist_from_C[point]:
                dist_from_C[point] = picked.dist_to(point)

            if dist_from_C[point] > max_d[-1]:
                max_d[-1] = dist_from_C[point]  #update max distance from current list of centers
                next_point = point  #update next point to pick (the farthest as now)
        picked = next_point
    max_d[-1] = 0
    return C, max_d

def build_test_points():
    X = []
    X.append(Point(1,1))
    X.append(Point(1,4))
    X.append(Point(0,0))
    X.append(Point(3,0))
    X.append(Point(2,2))
    X.append(Point(1,0))
    return X

def test():
    X = build_test_points()
    p, d = ex1(X)
    for i in range(len(p)):
        print(p[i], "[ max d =", d[i], "]")
