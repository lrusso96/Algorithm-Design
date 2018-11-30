import itertools
class Task:
    def __init__(self, t, c, descr=""):
        self.t = t
        self.c = c
        self.descr = descr
        
    def __str__(self):
        return self.descr + " at t" + str(self.t) + ": $" + str(self.c)

def build_test_tasks():
    tasks = []
    tasks.append(Task(1,[2], "medium"))
    tasks.append(Task(3,[1], "easy"))
    tasks.append(Task(3,[2], "medium"))
    tasks.append(Task(3,[3], "hard"))
    tasks.append(Task(7,[3], "hard"))
    tasks.append(Task(7,[2], "medium"))
    tasks.append(Task(8,[1], "easy"))
    return tasks

def init_cost(mask, hire):
    l = []
    l.append(mask.count("1")*hire)
    return l

def dynamic_matrix(T, k, hire):
    m = {}
    for mask in itertools.product("01", repeat=k):
        m[mask] = init_cost(mask, hire)

    for i in range(T):
        for mask in itertools.product("01", repeat=k):
            m[mask].append(-1)
    return m

def total_cost_of_freelance(tasks, freelancers):
    tot = 0
    for task in tasks:
        for f in freelancers:
            tot += task.c[f]
    return tot

def tot_cost(opt, tasks, mask_1, mask_2, hire, salary, severance):
    n_h = 0
    freelancers = []
    n_f=0
    for i in range(len(mask_1)):
        if mask_2[i] == "0":
            freelancers.append(i)
            if mask_1[i] == "1":
                n_f+=1
        elif mask_1[i] == "0":
            n_h+=1
            
    n_s = mask_2.count("1")
    return opt[mask_1] + hire*n_h + salary*n_s + severance*n_f + total_cost_of_freelance(tasks, freelancers)
        
def ex4_2(tasks, k, hire, salary, severance) :
    T = tasks[-1].t  # last instant of time
    m = dynamic_matrix(T, k, hire) 
    for i in range(1, T+1):
        current = []  # tasks at period i
        while len(tasks) > 0 and tasks[0].t == i:   # assume tasks are ordered!
            current.append(tasks.pop(0))
        opt = {}
        for mask in itertools.product("01", repeat=k):
            opt[mask] = m[mask][i-1]

        for mask_2 in itertools.product("01", repeat=k):
            for mask_1 in  itertools.product("01", repeat=k):
                val = tot_cost(opt, current, mask_1, mask_2, hire, salary, severance)
                if m[mask_2][i] == -1:
                    m[mask_2][i] = val
                else:
                    m[mask_2][i] = min(m[mask_2][i], val)
                #print(m[mask_2][i])

    first = True
    for mask in itertools.product("01", repeat=k):
        if first:
            ret = m[mask][T]
            first = False
        else:
            ret = min(ret, m[mask][T])
    print(m)
    return ret
        
        
def main():
    tasks = build_test_tasks()
    for task in tasks:
        print(task)
    return ex4_2(tasks, 1, 1,2, 2)
