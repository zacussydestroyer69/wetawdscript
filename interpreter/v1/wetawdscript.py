##                  Imports
import argparse
import os

##                  Tokenizer
#  (Valid) Token list
tokenlist = {
    "logicaloperators": [
        "==",
        "!="
    ],
    "definitiveoperators": [
        "=",
        "=+",
        "=-"
    ],
    "functions": [
        "write",
        "prompt",
        "clear",
        "break"
    ],
    "logicstatements" : [
        "if"
    ],
    "definitivestatements": [
        "set",
        "edit",
        "func"
    ]
}

#  Tokenize a code line
def tokenizeLine(codeline):
    lineTokens = []

    tokenizeWhitespace = codeline.split(" ")

    if str(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("(", "")) in tokenlist["functions"]:
        lineTokens.append(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("(", ""))
        if tokenizeWhitespace[0][len(tokenizeWhitespace[0]) - 1:] == "(":
            lineTokens.append("callfunc")
        else: 
            lineTokens.append("none")
        if len(tokenizeWhitespace) > 1:
            lineTokens.append(" ".join(tokenizeWhitespace[1:len(tokenizeWhitespace) - 1]))
        else: 
            lineTokens.append("none")
        if tokenizeWhitespace[len(tokenizeWhitespace) - 1][len(tokenizeWhitespace[len(tokenizeWhitespace) - 1]) - 1:] == ")":
            lineTokens.append("endcallfunc")
        else: 
            lineTokens.append("none")
    
    if str(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("{", "")) in tokenlist["logicstatements"]:
        lineTokens.append(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("{", ""))
        if tokenizeWhitespace[0][len(tokenizeWhitespace[0]) - 1:] == "{":
            lineTokens.append("statement")
        else: 
            lineTokens.append("none")
        if len(tokenizeWhitespace) > 1:
            lineTokens.append(" ".join(tokenizeWhitespace[1:len(tokenizeWhitespace) - 1]))
        else: 
            lineTokens.append("none")
        if tokenizeWhitespace[len(tokenizeWhitespace) - 1][len(tokenizeWhitespace[len(tokenizeWhitespace) - 1]) - 1:] == "}":
            lineTokens.append("endstatement")
        else: 
            lineTokens.append("none")

    if str(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("{", "")) in tokenlist["definitivestatements"]:
        lineTokens.append(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("{", ""))
        if tokenizeWhitespace[0][len(tokenizeWhitespace[0]) - 1:] == "{":
            lineTokens.append("statement")
        else: 
            lineTokens.append("none")
        if len(tokenizeWhitespace) > 1:
            lineTokens.append(" ".join(tokenizeWhitespace[1:len(tokenizeWhitespace) - 1]))
        else: 
            lineTokens.append("none")
        if tokenizeWhitespace[len(tokenizeWhitespace) - 1][len(tokenizeWhitespace[len(tokenizeWhitespace) - 1]) - 1:] == "}":
            lineTokens.append("endstatement")
        else: 
            lineTokens.append("none")
        
    if str(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("(", "")) in list(storedFuncs.keys()):
        lineTokens.append(tokenizeWhitespace[0][0:len(tokenizeWhitespace[0])].replace("(", ""))
        if tokenizeWhitespace[0][len(tokenizeWhitespace[0]) - 1:] == "(":
            lineTokens.append("callfunc")
        else: 
            lineTokens.append("none")
        if tokenizeWhitespace[len(tokenizeWhitespace) - 1][len(tokenizeWhitespace[len(tokenizeWhitespace) - 1]) - 1:] == ")":
            lineTokens.append("endcallfunc")
        else: 
            lineTokens.append("none")

    return lineTokens

##                  Totally Legit Interpreter That Is Also Kinda A Parser?
# Error things
def err(errcode, linenum = 0, code = "", var = ""):
    linenum = str(linenum)
    errors = {
        "nogivenfile": "\033[91mERROR: No file given! \n To open a file, open the source file for the crackscript compiler using the \"f\" and giving the directory to a .tard file. \n Or type a directory below.\033[00m",
        "wrongfiletype": "\033[91mERROR: A file with the wrong type was given! \n You need to specify a \".tard\" file!!\033[00m",
        "unassignedvar": "\033[91mERROR: Variable \"" + var + "\" undefined! \n ---[in line " + linenum + "] \"" + code +  "\" \n Assign a value to a variable before trying to read its value!!\033[00m",
        "promptnovargiven": "\033[91mERROR: No variable given to save prompt response! \n ---[in line " + linenum + "] \"" + code +  "\" \n Give a variable to save the prompt's response to. \n Example: \"prompt( enter something:, to var )\".\033[00m",
        "missingchar(": "\033[91mERROR: \"(\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When calling a function, use \"(\" and \")\" after the function identifier to hold arguments and call the function!\033[00m",
        "missingchar)": "\033[91mERROR: \")\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When calling a function, use \"(\" and \")\" after the function identifier to hold arguments and call the function!\033[00m",
        "missingchar()": "\033[91mERROR: \"(\" and \")\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When calling a function, use \"(\" and \")\" after the function identifier to hold arguments and call the function!\033[00m",
        "missingchar{": "\033[91mERROR: \"{\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When making a statement, use \"{\" and \"}\" to hold logical conditions and responses for if/else/then statements!\033[00m",
        "missingchar}": "\033[91mERROR: \"}\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When making a statement, use \"{\" and \"}\" to hold logical conditions and responses for if/else/then statements!\033[00m",
        "missingchar{\}": "\033[91mERROR: \"{\" and \"}\" expected! \n ---[in line " + linenum + "] \"" + code + "\" \n When making a statement, use \"{\" and \"}\" to hold logical conditions and responses for if/else/then statements!\033[00m",
    }
    print(errors[errcode])
    print("\033[0m")

#  The     I n t e r p a r s l e r
#  it checks if the syntax and shit is correct but also interprets it or something a
storedVars = {
    
}
storedFuncs = {

}

def compile(codelines):
    curLine = 0
    for item in codelines:
        curLine = curLine + 1
        lineTokens = tokenizeLine(item)
        if lineTokens[0] in tokenlist["functions"]:
            if lineTokens[1] == "none" and lineTokens[3] == "endcallfunc":
                err("missingchar(", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "callfunc" and lineTokens[3] == "none":
                err("missingchar)", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "none" and lineTokens[3] == "none":
                err("missingchar()", curLine, codelines[curLine - 1])
            else:
                keyword = lineTokens[0]

                if keyword == "write":
                    args = lineTokens[2].split("\\\\")
        
                    toPrint = args[0]
                    for item in args[0].split(" "):
                        if item[0] == "@":
                            if "".join(item[1::]) in storedVars:
                                toPrint = toPrint.replace(item, storedVars[item[1::]])
                            else:
                                toPrint = ""
                                err("unassignedvar", curLine, codelines[curLine - 1], item[1::])
                    print(toPrint)
                    
                if keyword == "prompt": 
                    args = lineTokens[2].split("to")
                    if len(args) == 2:
                        storedVars.update({args[1][1::]: input(args[0] + " ")})
                    else:
                        err("promptnovargiven", curLine, codelines[curLine - 1])

                if keyword == "clear":
                    os.system("cls")

                if keyword == "break":
                    print("")
                    
        if lineTokens[0] in tokenlist["logicstatements"]:
            if lineTokens[1] == "none" and lineTokens[3] == "endstatement":
                err("missingchar{", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "statement" and lineTokens[3] == "none":
                err("missingchar}", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "none" and lineTokens[3] == "none":
                err("missingchar{\}", curLine, codelines[curLine - 1])
            else:
                keyword = lineTokens[0]
                condition = lineTokens[2].split(":")[0]
                if len(condition.split(" ")) == 1 or len (condition.split(" ")) == 2:
                    return
                elif len(condition.split(" ")) == 3:
                    identifiers = [condition.split(" ")[0], condition.split(" ")[2]]
                    if "".join(identifiers[0][1::]) in storedVars:
                        identifiers[0] = identifiers[0].replace(identifiers[0], storedVars[identifiers[0][1::]])
                    else:
                        identifiers[0] = ""
                        err("unassignedvar", curLine, codelines[curLine - 1], identifiers[0][1::])
                if identifiers[1][0] == "@":
                    if "".join(identifiers[1][1::]) in storedVars:
                        identifiers[1] = identifiers[1].replace(identifiers[1], storedVars[identifiers[1][1::]])
                    else:
                        identifiers[1] = ""
                        err("unassignedvar", curLine, codelines[curLine - 1], identifiers[0][1::])
                operator = condition.split(" ")[1]
                if len(lineTokens[2].split(":")) >= 2:
                    then = lineTokens[2].split(":")[1][1::]
                if len(lineTokens[2].split(":")) == 3:
                    elsethen = lineTokens[2].split(":")[2][1::]

                if keyword == "if":
                    if operator in tokenlist["logicaloperators"]:
                        if operator == "==":
                            if identifiers[0] == identifiers[1]:
                                compile([then])
                            else:
                                compile([elsethen])
                        if operator == "!=":
                            if identifiers[0] != identifiers[1]:
                                compile([then])
                            else:
                                compile([elsethen])

        if lineTokens[0] in tokenlist["definitivestatements"]:
            if lineTokens[1] == "none" and lineTokens[3] == "endstatement":
                err("missingchar{", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "statement" and lineTokens[3] == "none":
                err("missingchar}", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "none" and lineTokens[3] == "none":
                err("missingchar{\}", curLine, codelines[curLine - 1])
            else:
                keyword = lineTokens[0]
                identifier = lineTokens[2].split("=")[0].replace(" ", "")
                setValue = lineTokens[2].split("=")[1]
                
                if keyword == "set":
                    if setValue[0] == "@":
                        if setValue[1::] in storedVars:
                            value = storedVars[setValue[1::]]
                    else: 
                        value = setValue[1::]
                    storedVars.update({identifier: value})
                if keyword == "edit":
                    if setValue[0] == "@":
                        if setValue[1::] in storedVars:
                            value = storedVars[setValue[1::]]
                    else: 
                        value = setValue[1::]
                    storedVars[identifier] = value

                if keyword == "func":
                    value = setValue[1::]
                    storedFuncs.update({identifier: value.split("; ")})
                    
        if lineTokens[0] in list(storedFuncs.keys()):
            if lineTokens[1] == "none" and lineTokens[2] == "endcallfunc":
                err("missingchar(", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "callfunc" and lineTokens[2] == "none":
                err("missingchar)", curLine, codelines[curLine - 1])
            elif lineTokens[1] == "none" and lineTokens[2] == "none":
                err("missingchar()", curLine, codelines[curLine - 1])
            else:
                keyword = lineTokens[0]
                compile(storedFuncs[keyword])

##                  Start compiling given file
parser = argparse.ArgumentParser(add_help = False, exit_on_error = True)
parser.add_argument('open', metavar = "f", type = str, nargs = "?")
args = parser.parse_args()

if type(args.open) == str:
    print(args.open.split(".")[1])
    if args.open.split(".")[1] == "tard":
        with open(args.open) as file:
            os.system("cls")
            lines = "".join(file.readlines()).split("\n")
            compile(lines)
    else:
        err("wrongfiletype")
else:
    err("nogivenfile")
    with open(input("> ")) as file:
            os.system("cls")
            lines = "".join(file.readlines()).split("\n")
            compile(lines)