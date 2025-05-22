import re
import json
def replace_negatives(expression):
    pattern = r'\((\s*-\s*\d+\s*)\)' 
    
    def replacer(match):
        number = match.group(1)
        return f"({number}: ℝ )" 
    new_expression = re.sub(pattern, replacer, expression)
    return new_expression

def _replace(expression):
    len_ = len(expression)
    flag = 0 
    kuohao = 0
    i = 0
    new_expression = ""
    while i < len_:
        c = expression[i]
    # print(i)
        new_expression += c
        if (not flag) and c=='↑':
            if expression[i+1] == '(':
                new_expression = new_expression[:-1]
                flag = 1
            else:
                new_expression = new_expression[:-1] + '( '
                flag = 2
            i+=1
            continue
        if flag == 1:
            if c == '(':kuohao+=1
            elif c==')':kuohao-=1
            if not kuohao:
                new_expression = new_expression[:-1] + ':ℝ )'
                flag = 0
        elif flag == 2:
            if c==' ' or c=='\n' or i == len_-1:
                new_expression = new_expression +':ℝ )'
                flag = 0
        i+=1
    return new_expression
def repair(exp,neg=False):
    if neg:return replace_negatives(exp)
    return _replace(replace_negatives(exp))
def find_all_occurrences(s, substring):
    positions = []
    start = 0
    while True:
        idx = s.find(substring, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + 1
    return positions
def repair_stat(stat:str):
    stat = stat.replace(" ","")
    stat = re.sub(r'\+0(?![\*/])', '', stat)
    stat = re.sub(r'\-0(?![\*/])', '', stat)
    stat = re.sub(r'(?<![\*/])0\+', '', stat)
    stat = stat.replace("/1","")
    stat = stat.replace("*1","")
    stat = stat.replace("1*","")
    def remove_redundant_brackets(expression):
        stack = []
        pairs = []
        mp = dict()
        for i, char in enumerate(expression):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if stack:
                    open_idx = stack.pop()
                    pairs.append((open_idx, i))
        for st,ed in pairs:
            if st>0 and expression[st-1]=='(' and ed<len(expression)-1 and expression[ed+1]==')':
                continue
            for i in range(st,ed+1):
                if expression[i]=='*' or expression[i]=='/' or expression[i]=='+' or expression[i]=='-':
                    mp[st]=1
                    mp[ed]=1
                    break
        new_expression = ""
        for i in range(len(expression)):
            if (expression[i]=='(' or expression[i]==')') and i not in mp.keys():
                continue
            new_expression+=expression[i]
        return new_expression
    stat = remove_redundant_brackets(stat)
    return stat

