

#finds a set of related instructions to a given list of ingredients

import random
import json

#if __name__ == "__main__":

    

def find_ins_set ( ingr_lst ):
    f = open("instructions.txt","r")
    to_d = f.read()
    lst = json.loads(to_d)
    ins_set = {}
    ins_set['none'] = []
    for ins in lst:
        i_lst = ins['ingredients']
        include = True
        for i in i_lst:
            if not i in ingr_lst:
                include = False
        if include:
            for i in i_lst:
                if not i in ins_set:
                    ins_set[i] = []
                ins_set[i] += [ins]
                
        if len(i_lst) == 0:
            ins_set['none'].append(ins)

    return ins_set

def refine_ins_set ( ins_set ):
    #pass the result of find_ins_set to this function
    
    acc = []
    for item in ins_set:
        if item != 'none':
            randy = random.random()
            if(randy < 0.5):
                acc.extend(random.sample(ins_set[item], min(1, len(ins_set[item])-1)))
            elif(randy < 0.83):
                acc.extend(random.sample(ins_set[item], min(2, len(ins_set[item])-1)))
            else:
                acc.extend(random.sample(ins_set[item], min(3, len(ins_set[item])-1)))
        else:
            acc.extend(random.sample(ins_set[item], int(random.random()*5)))

    final_lst = []
    while len(acc) != 0:
        cur_min = 1.0
        cur_item = None
        for i,item in enumerate(acc):
            if item['relative_position'] <= cur_min:
                cur_min = item['relative_position']
                cur_item = item
        final_lst.append(cur_item['instruction'])
        acc.remove(cur_item)

    if not "serve" in final_lst[-1].lower():
        final_lst.append(u"Serve")
    return final_lst
