import itertools
class Task:
    def __init__(self, t, outsources, skills, descr=""):
        self.t = t
        self.outsources = outsources
        self.skills = skills
        self.descr = descr
        
    def __str__(self):
        return self.descr + " at t" + str(self.t) + ": $" + str(self.outsources)

def initial_cost(mask, hire):
    hire_cost = 0
    for i in range(len(mask)):
        if mask[i] == "1":
            hire_cost += hire[i]
    return [ hire_cost ]

def dynamic_matrix(T, hire):
    m = [[0],[hire]]
    for i in range(T):
        m[0].append(-1)
        m[1].append(-1)
    return m

    for i in range(T):
        for mask in masks:
            m[mask].append(None)
    return m

def total_cost_of_freelance(tasks, k):
    tot = 0
    for task in tasks:
        tot += task.skills[k] * task.outsources[k]
    return tot
        
def ex4_2(tasks, k, hire, salary, severance) :
    ret = 0
    T = tasks[-1].t  # last instant of time
    for j in range(k):
        tasks_t = tasks.copy()
        m = dynamic_matrix(T, hire[j]) 
        for i in range(1, T+1):
            current = []  # tasks at period i
            while len(tasks_t) > 0 and tasks_t[0].t == i:   # assume tasks are ordered!
                current.append(tasks_t.pop(0))
            opt1 = m[0][i-1]     
            opt2 = m[1][i-1]     
            m[0][i] = total_cost_of_freelance(current, j) + min(opt1, opt2 + severance[j])
            m[1][i] = salary[j] + min(opt1 + hire[j], opt2)
        #m[1][T] += severance  # necessary if the company wants to fire everyone at the end of T!
        ret += min(m[0][T], m[1][T])
        print(m)
    return(ret)

def build_test_tasks():
    tasks = []
    tasks.append(Task(1, 2, [0, 1], "medium"))
    tasks.append(Task(3, 1, [1, 0], "easy"))
    tasks.append(Task(3, 2, [0, 1], "medium"))
    tasks.append(Task(3, 3, [1, 1], "hard"))
    tasks.append(Task(7, 3, [1, 0], "hard"))
    tasks.append(Task(7, 2, [1, 0], "medium"))
    tasks.append(Task(8, 1, [1, 0], "easy"))
    return tasks

def build_Fioraldi_tasks():
    tasks = []
    tasks.append(Task(1, [3,3], [1, 1], "medium"))
    tasks.append(Task(1, [2,2], [1, 0], "easy"))
    tasks.append(Task(2, [6,6], [1,0], "hard"))
    tasks.append(Task(5, [1,1], [0, 1], "easy"))
    tasks.append(Task(7, [1,1], [0, 1], "easy"))
    tasks.append(Task(9, [7,7], [1, 1], "hard"))
    return tasks       

def test():
    tasks = build_Fioraldi_tasks()
    for task in tasks:
        print(task)

    # k=2
    hire = [2,2]    #same for skill1 and skill2
    salary = [2,2]    #skill2 has higher salary
    severance = [3,3]    #same for skill1 and skill2
    ret = ex4_2(tasks, 2, hire, salary, severance)
    print("Min cost is", ret)
