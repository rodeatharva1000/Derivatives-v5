#for trig use
trig_helper_dict = {"sin" : "cos()", 
                    "cos" : "-sin()", 
                    "tan" : "sec**2()", 
                    "cot": "-csc**2()", 
                    "sec" : "sec()*tan()", 
                    "csc" : "-csc()*cot()",

                    "sininv"   : "1/sqrt(1 - ()**2)",
                    "cosinv"   : "-1/sqrt(1 - ()**2)",
                    "taninv"   : "1/(1 + ()**2)",
                    "cotinv"   : "-1/(1 + ()**2)",
                    "secinv"   : "1/(()sqrt(())*2 - 1))",
                    "cscinv" : "-1/(())sqrt(())*2 - 1))",
                    }


def exprecdev(exprinp):
    def uvstacksplit(exprinp):
        open = 0
        for i, c in enumerate(exprinp):
            if c == "(": open += 1
            elif c == ")": open -= 1

            if open: continue

            #inner utility 1
            inginp = exprinp[1:i]
        
            #if further exists
            if (i+3)<len(exprinp):
                #operation + and -
                if exprinp[i+1] in ("+", "-"): return f"({exprecdev(inginp)}){exprinp[i+1]}({exprecdev(exprinp[i+3:-1])})"
                
                #inner utility 2
                inginp2 = exprinp[i+3:-1]
               
                idx, prefix = 0, ""
                prefix += "("
                while idx<len(inginp) and (inginp[idx].isdigit() or inginp[idx] == "-"):
                    if inginp[idx] == "-": prefix += "(-)"
                    else: prefix += f"{inginp[idx]}"
                    idx += 1
                prefix += ")"
                inginp = inginp[idx:]
                idx = 0
                prefix += "("
                while idx<len(inginp2) and (inginp2[idx].isdigit() or inginp2[idx] == "-"):
                    if inginp2[idx] == "-": prefix += "(-)"
                    else: prefix += f"{inginp2[idx]}"
                    idx += 1
                prefix += ")"
                prefix = prefix.replace("()", "")
                inginp2 = inginp2[idx:]
                
                #operation *
                print(inginp2)
                if exprinp[i+1] == "*": 
                    if "x" not in inginp:
                        return f"(({prefix})({exprecdev(inginp2)}))"
                    elif "x" not in inginp2:
                        return f"(({prefix})({exprecdev(inginp)}))"
                    return f"(({prefix})(({exprecdev(inginp)})({inginp2}))+(({inginp})({exprecdev(inginp2)})))"
                
                #operation /
                elif exprinp[i+1] == "/": 
                    if "x" not in inginp:
                        return f"(({prefix})(one-by({inginp2})({exprecdev(inginp2)}))"
                    if "x" not in inginp2:
                        return f"(({prefix})({inginp})({exprecdev({inginp})}))"
                    return f"(({prefix})((({exprecdev(inginp)})({inginp2}))-(({inginp})({exprecdev(inginp2)})) / ({(inginp2)}-pow(2))))"


    #const
    if "x" not in exprinp: return "(0)"

    #x
    elif exprinp == "x": return "(1)"

    #mul-fact
    elif exprinp[0].isdigit():
        ptr = 0
        while exprinp[ptr].isdigit(): ptr += 1
        return f"(({exprinp[:ptr]})({exprecdev(exprinp[ptr:])}))"
    
    #min
    elif exprinp[0] == "-": return f"((-1)({exprecdev(exprinp[1:])}))"
    

    #uv  splits
    if exprinp[0] == '(':
        stacksp = uvstacksplit(exprinp)
        if stacksp: return stacksp

    #outer utility
    input_list = exprinp.split("(") 


    #a pow x
    if input_list[0] == "a-pow":
        idx = exprinp.find(",")
        a, x = exprinp[6:idx], exprinp[idx+1:-1]
        return f"({a}-pow({x})log({a})({exprecdev(x)}))"
    
    #x pow n
    elif input_list[0] == "x-pow":
        idx = exprinp.rfind(",")
        x, n = exprinp[6:idx], exprinp[idx+1:-1]
        return f"(({n})({x}-pow({int(n)-1}))({exprecdev(x)}))"
        
    #one by
    elif input_list[0] == "one-by":
        x = exprinp[7:-1]
        return f"((one-by({x}-pow(2)))({exprecdev(x)}))"

    #e pow x
    elif input_list[0] == "e-pow":
        x = exprinp[6:-1]
        return f"((e-pow({x}))({exprecdev(x)}))"
    
    #x pow x
    elif input_list[0] == "x-powx":
        x = exprinp[7:-1]
        return f"(({x}-pow({x}))({exprecdev(x)}))"

    #log
    elif input_list[0] == "log" :
        x = exprinp[4:-1]
        return f"((1/{x})({exprecdev(x)}))"

    #trig and inv-trig
    elif input_list[0] in trig_helper_dict:
        x, idx = "", exprinp.find("(")
        x = exprinp[idx+1:-1]
        return f"{trig_helper_dict[input_list[0]].replace('()', f'({x})')}({exprecdev(x)})"

print("Input Must Be In Valid Format - Input Instruction Document(Pending)")
print("derivative of y will br found strictly w.r.t x")
print("Input Example")
print("10sin(x)")
print("(cot(x))+(sec(x))")
print("(9cot(3x))+(2sec(8x))")
print("(9cot(3x))/(2sec(8x))")
print("sin(cos(10tan(log(2x))))")
print("(sin(cos(10tan(log(2x)))))+(log(x))")
print("(sin(cos(10tan(log(2x)))))/(log(x))")

exprinp  = ""
while exprinp != "stop":
    exprinp = input("Enter Equation y (to stop - enter(stop)) to find d/dx: ").replace(" ", "")
    temp_ans = exprecdev(exprinp).replace("()", "")
    print(temp_ans)
