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
    pos_s=''
    j = 0
    n = len(s)
    for j in range(n):
        i=s[j]
        if i.isalnum():
            pos_s+=i
        elif i == '(':
            stk.append(i)
        elif i == ')':
            while stk and stk[-1] != '(':
                pos_s+=stk.pop()
            stk.pop()  

        else:
            if not stk:
                stk.append(i)
            else:
                while stk and (prec(i) < prec(stk[-1]) or (prec(i) == prec(stk[-1]) and assoc(i) == 'L')):
                    pos_s+=stk.pop()
                stk.append(i)
    while stk:
        pos_s+=stk.pop()
    return pos_s;
if __name__ == "__main__":
    s = input("Enter exp:").strip()
    flag = 0
    if '=' in s:
        lhs,s = map(str,s.split("="))
        lhs,s = lhs.strip(),s.strip()
        flag = 1
    pos_s= inftopost(s)
    stk = []
    i = 0
    op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
    df = {'Opnd':[],'arg1':[],'arg2':[],'res':[]}
    if flag:
        pos_s = lhs + pos_s + "="
    for j in pos_s:
        if j.isalnum():
            stk.append(j)
        else:
            b = stk.pop()
            a = stk.pop()
            if j == '=':
                print(a,j,b)
                df['Opnd'].append(op[j])
                df['arg1'].append(b)
                df['arg2'].append('')
                df['res'].append(a)
                continue;
            temp = f'temp{i}'
            print(temp," = ",a,j,b)
            df['Opnd'].append(op[j])
            df['arg1'].append(a)
            df['arg2'].append(b)
            df['res'].append(temp)
            stk.append(temp)
            i+=1
    df = pd.DataFrame(df)
    print(df)

