import pandas as pd
import numpy as np
import math
import re,string

def tokenize(text,symbol = False):
        text_f = open(text)
        data = text_f.readlines()
        text_f.close()
        n_type = int(data[0].split()[0])
        _type = {}
        trans = {}
        for i in range(1,n_type+1):
            if symbol:
                _type[data[i].strip()]=i-1
            trans[i-1]={}
        for i in range(n_type+1,len(data)):
            trans[int(data[i].split()[0])][int(data[i].split()[1])]=int(data[i].split()[2])
        return n_type,_type, trans
    
def data_preprocess(State_File, Symbol_File, Query_File):
    
    state_n, states, trans = tokenize(State_File)
    symbol_n, symbol, emission = tokenize(Symbol_File, True)

    #transformation_probability
    trans_p = np.zeros((state_n-1,state_n-1))
    for i in range(state_n-1):
        for x in range(state_n-1):
            if x == state_n-2: j = x+1
            else: j = x
            try: trans_p[i][x] =(trans[i][j]+1)/(sum(trans[i].values())+state_n-1)
            except KeyError:
                trans_p[i][x] = 1/(sum(trans[i].values())+state_n-1)
    #store squences
    obs = []
    with open(Query_File) as query:
        for line in query.readlines():
            tokens =list(filter(None,re.split(r"([(])|([)])|(-)|(&)|(/)|(,)|\s+",line)))
            obs.append(tokens) 
    return state_n, states,trans,symbol_n, symbol, emission,trans_p,obs


def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
    
    state_n, states,trans,symbol_n, symbol, emission,trans_p,obs=data_preprocess(State_File, Symbol_File, Query_File)                              
    #Q1: opt_probabilities
    viterbi = []
    for seq in obs:
        viterbi.append([])
        viterbi[-1].append(state_n-2)
        opt_path = {}
        
        for i in range(state_n-2): opt_path[i] = [i] 
        opt = np.zeros(state_n-2)
        for i in range(state_n-2):
            try: 
                emis_p = (emission[i][symbol[seq[0]]]+1)/(sum(emission[i].values())+symbol_n+1)
                opt[i] = (math.log(trans_p[state_n-2][i]) + math.log(emis_p)) 
            except KeyError: 
                opt[i] = math.log(trans_p[state_n-2][i]) - math.log((sum(emission[i].values())+symbol_n+1))
        
        for i in range(1,len(seq)):
            path ={}
            current_opt= np.zeros(state_n-2)
            for j in range(state_n-2):
                (prob, state) = \
                    max([(opt[k]+math.log(trans_p[k][j]),k) for k in range(state_n-2)])
                path[j] = opt_path[state] + [j]
                try:
                    emis_p = (emission[j][symbol[seq[i]]]+1)/(sum(emission[j].values())+symbol_n+1)
                    current_opt[j] = math.log(emis_p)+prob
                except KeyError:
                    current_opt[j] = prob-math.log((sum(emission[j].values())+symbol_n+1))
                
            opt_path = path
            opt = current_opt
        (prob, state) = max([(opt[k]+math.log(trans_p[k][-1]),k) for k in range(state_n-2)])
        viterbi[-1]+=opt_path[state]
        viterbi[-1].append(state_n-1)
        viterbi[-1].append(prob)
    return viterbi

def quick_sort(value, paths, left, right):
    if left < right:
        mid = partition(value, paths, left, right)
        quick_sort(value, paths, left,  mid-1)
        quick_sort(value, paths, mid+1, right)

def partition(value, paths, left, right):
    tmp_v = value[left]
    v_index = left
    tmp_p = paths[left]
    while left < right:
        while left < right and (value[right] > tmp_v or (value[right] == tmp_v and tie(right,v_index,paths,paths))):
            right -= 1
        value[left] = value[right]
        paths[left] = paths[right]
        while left < right and (value[left] < tmp_v or (value[left] == tmp_v and tie(v_index,left,paths,paths))):
            left += 1
        value[right] = value[left]
        paths[right] = paths[left]
    value[left] = tmp_v
    paths[left] = tmp_p
    return left

def swap(arr1,arr2,x,y):
    temp1,temp2 = arr1[x],arr2[x]
    arr1[x],arr2[x] = arr1[y],arr2[y]
    arr1[y],arr2[y] = temp1,temp2

def tie(x,y,path1,path2,new_comparasion=False):
    old = -1
    new = -2
    if not new_comparasion:
        new = -1     
    while (old + len(path1[x])) > -1:
        if path1[x][old] < path2[y][new]:
            return True
            break
        elif path1[x][old] == path2[y][new]:
            old -= 1
            new -= 1
        else:
            break
    return False
def heap_sort(parent,size,heap,heap_path):
    child = parent * 2 + 1
    while (child<size):
        if (child+1) < size and heap[child] > heap[child+1]:
                child +=1
        #print(heap)
        if  heap[parent] > heap[child] or \
            (heap[parent] == heap[child] and tie(parent,child,heap_path,heap_path)):
            swap(heap,heap_path,parent,child)
            parent = child
            child = 2 * parent + 1
        else:
            break
                
def top_k(temp,opt_path,k,j=[]):
    temp = np.array(temp).reshape(-1,1)
    opt_path = np.array(opt_path).reshape(len(temp),-1).tolist()
    heap = [temp[i] for i in range(k)]
    heap_path = [opt_path[i] + j for i in range(k)]
    for i in range(int((k-2)/2),-1,-1):
        heap_sort(i,k,heap,heap_path)
    for i in range(k,len(temp)):
        if heap[0] < temp[i] or (heap[0] == temp[i] and tie(i,0,opt_path,heap_path,j!=[])):
            heap[0] = temp[i]
           # print(j,len(temp),len(opt_path),opt_path)
            heap_path[0] = opt_path[i]+j
            heap_sort(0,k,heap,heap_path)
    return  heap,heap_path

def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
    state_n, states,trans,symbol_n, symbol, emission,trans_p,obs=data_preprocess(State_File, Symbol_File, Query_File)
    viterbi = []
    for seq in obs:
        opt_path = [[i] for i in range(state_n-2)] 
        opt =  {}
        for i in range(state_n-2):
            opt[i]=[]
        for i in range(state_n-2):
            try: 
                emis_p = (emission[i][symbol[seq[0]]]+1)/(sum(emission[i].values())+symbol_n+1)
                opt[i].append(math.log(emis_p) + math.log(trans_p[state_n-2][i]))
            except KeyError: 
                opt[i].append(math.log(trans_p[state_n-2][i]) -math.log((sum(emission[i].values())+symbol_n+1)))
        current_k = 1    
        for i in range(1,len(seq)):
            path =[]
            if k > current_k *(state_n-2): 
                current_k *= state_n-2
            else: current_k = k
            current_opt= []
            for j in range(state_n-2):
                temp = []
                for sta in range(state_n-2):
                    for prev_opt in opt[sta]:         
                        temp.append(prev_opt + math.log(trans_p[sta][j]))
                (prob, state) = top_k(temp,opt_path,current_k,[j])
                path.append(state)
                try:
                    emis_p = (emission[j][symbol[seq[i]]]+1)/(sum(emission[j].values())+symbol_n+1)
                    current_opt.append(math.log(emis_p)+np.array(prob))
                except KeyError:
                    current_opt.append(np.array(prob)-math.log((sum(emission[j].values())+symbol_n+1)))
            opt_path = path
            opt = current_opt 
        for x in range(state_n-2):
            opt[x] += math.log(trans_p[x][-1])
       # print(current_k,len(opt),len(opt_path))
        (prob, state) = top_k(opt,opt_path,k)
        prob = np.array(prob).reshape(-1,1).tolist()
        #print(len(prob),len(state))
        quick_sort(prob,state,0,k-1)
        for x in range(k-1,-1,-1):
            viterbi.append([])
            viterbi[-1].append(state_n-2)
            viterbi[-1]+= state[x]
            viterbi[-1].append(state_n-1)
            viterbi[-1].append(prob[x][0])
        #print(obs)
    return viterbi

