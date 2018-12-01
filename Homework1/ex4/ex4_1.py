class Task:
    def __init__(self, t, c, descr=""):
        self.t = t
        self.c = c
        self.descr = descr
        
    def __str__(self):
        return self.descr + " at t" + str(self.t) + ": $" + str(self.c)

def build_test_tasks():
    tasks = []
    tasks.append(Task(1,2, "medium"))
    tasks.append(Task(3,1, "easy"))
    tasks.append(Task(3,2, "medium"))
    tasks.append(Task(3,3, "hard"))
    tasks.append(Task(7,3, "hard"))
    tasks.append(Task(7,2, "medium"))
    tasks.append(Task(8,1, "easy"))
    return tasks

def dynamic_matrix(T, hire):
    m = [[0],[hire]]
    for i in range(T):
        m[0].append(-1)
        m[1].append(-1)
    return m

def total_cost_of_freelance(tasks):
    tot = 0
    for task in tasks:
        tot += task.c
    return tot
        
def ex4_1(tasks, hire,, salary, severance):
    T = tasks[-1].t  # last instant of time
    m = dynamic_matrix(T, hire) 
    for i in range(1, T+1):
        current = []  # tasks at period i
        while len(tasks) > 0 and tasks[0].t == i:   # assume tasks are ordered!
            current.append(tasks.pop(0))
        op1 = m[0][i-1] 
        op2 = m[1][i-1] 
        m[0][i] = total_cost_of_freelance(current) + min(op1, op2 + severance)
        m[1][i] = salary + min(op1 + hire, op2)
    #m[1][T] += severance  # necessary if the company wants to fire everyone at the end of T!
    print(m)
    return min(m[0][T], m[1][T])

def test():
    tasks = build_test_tasks()
    for task in tasks:
        print(task)
    return ex4_1(tasks, 1,2,2)
