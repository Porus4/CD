import re
import pandas as pd
def prec(i):
    if i=='^':
        return 3;
    if i == '*' or i == '/':
        return 2;
    if i == '+' or i == '-':
        return 1;
    else:
        return -1;
def assoc(c):
    if c == '^':
        return 'R'
    return 'L'
def inftopost(s):
    stk = []
    pos_s = []
    j = 0
    n = len(s)
    ops = ['=','+','-','*','/','^']
    for j in range(n):
        i = s[j]
        if i in ops:
            if not stk:
                stk.append(i)
            else:
                while stk and (prec(i) < prec(stk[-1]) or (prec(i) == prec(stk[-1]) and assoc(i) == 'L')):
                    pos_s.append(stk.pop())
                stk.append(i)
        elif i == '(':
            stk.append(i)
        elif i == ')':
            while stk and stk[-1] != '(':
                pos_s.append(stk.pop())
            stk.pop()  

        else:
            pos_s.append(i)
            
    while stk:
        pos_s+=stk.pop()
    return pos_s;
def print_tree(tree, level=0):
    if isinstance(tree, list):
        print_tree(tree[2], level + 1)
        print('    ' * level + str(tree[0]))
        print_tree(tree[1], level + 1)
    else:
        if tree:
            print('    ' * level + str(tree))
def lex(ids,ops):
    ref = {}
    ops.append('')
    i = 1
    s=''
    for id in ids:
        s+=f"id{i} {ops[i-1]} "
        if re.match(r"[0-9]+",id[1]):
            ref[f"id{i}"] = id[1]
        i+=1
    return s,ref;
def syntax(pos_s):
    stack = []
    for token in pos_s:
        if re.match(r"[a-zA-Z0-9]+", token):
            stack.append(token)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append([token, operand1, operand2])
    return print_tree(stack[0])
def semantic(pos_s,ref):
    for i in range(len(pos_s)):
        if pos_s[i] in ref:
            pos_s[i] = ref[pos_s[i]] 
    return syntax(pos_s);
def Intermediate(pos_s):
    stk = []
    i = 0
    op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
    df = {'Opnd':list(),'arg1':list(),'arg2':list(),'res':list()}
    for j in pos_s:
        if re.match(r"[a-zA-Z0-9]+",j) or j[0] == '#':
            stk.append(j)
        else:
            b = stk.pop()
            a = stk.pop()
            temp = f'temp{i}'
            df['Opnd'].append(op[j])
            df['arg1'].append(a)
            df['arg2'].append(b)
            df['res'].append(temp)
            stk.append(temp)
            i+=1
    df = pd.DataFrame(df)
    return df;    
if __name__ == "__main__":
    inp = input()
    a = list(map(str,inp.split(" ")))
    op = {'=':'equ','+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow'}
    ops = []
    ids = []
    nums =[]
    j = 0
    for i in a:
        if i in op:
            ops.append(i)
            a.remove(i)
    for i in a:
        if re.match("[0-9]+",i):
            ids.append((j,i))
            nums.append((j,i))
            j+=1
        elif re.match("[a-zA-Z0-9]+",i):
            ids.append((j,i))
            j+=1
    lex_out,ref = lex(ids,ops)
    print("After passing through lexical analyser:\n")
    print(lex_out)
    flag = 0
    s = lex_out.split(" ")
    if '=' in lex_out:
        lhs,s = map(str,lex_out.split("="))
        lhs,s = lhs.strip(),s.strip().split(" ")
        flag = 1
    pos_s= inftopost(s)
    print(pos_s)
    i = 0
    op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
    df = {'Opnd':[],'arg1':[],'arg2':[],'res':[]}
    if flag:
        pos_s.insert(0,lhs)
        pos_s.append('=')
    print("After Synatx analyser:\n")
    syntax(pos_s)
    print("After Semantic Analyser:\n")
    semantic(pos_s,ref)
    for i in range(len(pos_s)):
        if pos_s[i] in ref:
            pos_s[i] = '#'+ref[pos_s[i]]
    print("\nAfter Intermediate Code Generation:\n")
    print(Intermediate(pos_s))
