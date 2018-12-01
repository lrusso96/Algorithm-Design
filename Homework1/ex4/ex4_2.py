import itertools
class Task:
    def __init__(self, t, outsource, skills, descr=""):
        self.t = t
        self.outsource = outsource
        self.skills = skills
        self.descr = descr
        
    def __str__(self):
        return self.descr + " at t" + str(self.t) + ": $" + str(self.outsource)

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

def init_cost(mask, hire):
    hire_cost = 0
    for i in range(len(mask)):
        if mask[i] == "1":
            hire_cost += hire[i]
    return [ hire_cost ]

def dynamic_matrix(T, masks, hire):
    m = {}
    for mask in masks:
        m[mask] = init_cost(mask, hire)

    for i in range(T):
        for mask in masks:
            m[mask].append(None)
    return m

def total_cost_of_freelance(tasks, freelancers):
    tot = 0
    for task in tasks:
        for f in freelancers:
            tot += task.skills[f] * task.outsource
    return tot

def total_cost_of_salary(salary, hired):
    tot = 0
    for h in hired:
        tot += salary[h]
    return tot

def total_cost_of_hire(hire, hiring):
    tot = 0
    for h in hiring:
        tot += hire[h]
    return tot

def total_cost_of_severance(severance, firing):
    tot = 0
    for f in firing:
        tot += severance[f]
    return tot

def total_cost(opt, tasks, mask_1, mask_2, hire, salary, severance):
    freelancers = []
    hiring = []
    hired = []
    firing = []
    for i in range(len(mask_1)):
        if mask_2[i] == "0":
            freelancers.append(i)
            if mask_1[i] == "1":
                firing.append(i)
        else:
            hired.append(i)
            if mask_1[i] == "0":
                hiring.append(i)

    c1 = total_cost_of_hire(hire, hiring)
    c2 = total_cost_of_salary(salary, hired)
    c3 = total_cost_of_severance(severance, firing)
    c4 = total_cost_of_freelance(tasks, freelancers)
    return opt[mask_1] + c1 + c2 + c3 + c4
        
def ex4_2(tasks, k, hire, salary, severance) :
    masks = []
    for mask in itertools.product("01", repeat=k):
        masks.append(mask)

    T = tasks[-1].t  # last instant of time
    m = dynamic_matrix(T, masks, hire) 
    for i in range(1, T+1):
        current = []  # tasks at period i
        while len(tasks) > 0 and tasks[0].t == i:   # assume tasks are ordered!
            current.append(tasks.pop(0))
        opt = {}
        for mask in masks:
            opt[mask] = m[mask][i-1]

        for mask_2 in masks:
            for mask_1 in  masks:
                val = total_cost(opt, current, mask_1, mask_2, hire, salary, severance)
                if m[mask_2][i] == None:
                    m[mask_2][i] = val
                else:
                    m[mask_2][i] = min(m[mask_2][i], val)

    ret = None
    for mask in masks:
        if ret == None:
            ret = m[mask][T]
        else:
            ret = min(ret, m[mask][T])
    print(m)
    return ret
       
def test():
    tasks = build_test_tasks()
    for task in tasks:
        print(task)
    hire = [1,1]    #same for skill1 and skill2
    salary = [2,3]    #skill2 has higher salary
    severance = [2,2]    #same for skill1 and skill2
    return ex4_2(tasks, 2, hire, salary, severance)
