# ------------ IMPORT MODULES ---------------/

import mysql.connector

# ------------- MORE IDEAS ------------------/

# TODO rather than printing the mysql output store them in variables
# TODO add if else statements
# TODO add a feature  that allows the user to pause the code for x amount of time

# --------------------------------------------------- FILE TO LIST OF COMMANDS ----------------------------------------/

# Get the content from the file and store it in a array named content
content = []

# count the number of lines in the list
with open("x.rdh", "r") as file:
    Content_ = file.read()
    Content_ = Content_.split("\n")
    while "" in Content_:
        Content_.remove("")
    count = 0
    for i in Content_:
        count += 1

# Filter the content in the array named commands
commands = []
for i in Content_:
    if "\n" in i:
        i = i.replace('\n', '')
    commands.append(i)

# sorts out the code word by word
commands_ = []
for i in range(0, len(commands)):
    commands_.append([])
    word = ""
    for j in commands[i]:
        if len(word) > 1 and j == "'":
            word += "'"
            commands_[i].append(word)
            word = ""
        elif j != " ":
            word += j
        else:
            if len(word) > 0:
                if word[0] != "'":
                    if word != "":
                        commands_[i].append(word)
                    word = ""
                else:
                    word += " "
    if word != "":
        commands_[i].append(word)


# ----------------X-------------------X-------------- FILE TO LIST OF COMMANDS -----------X---------------X------------/

# --------------------------------------------------- PROCESSING OUTPUT COMMANDS --------------------------------------/

# displays the command
# format:
# show '<string>'
def showCommand(command_, lineNum):
    # prints the given string or variable
    operators = ['+', '-', '/', '*']
    string_to_return = ""
    numString = []
    for i in range(1, len(command_)):
        # print the variable name
        if command_[i] in var_list:
            if var_list[command_[i]].isdigit() or var_list[command_[i]] in operators:
                if i + 1 >= len(command_):
                    numString.append(str(var_list[command_[i]]))
                    string_to_return += digitResult(numString, lineNum)
                elif not command_[i + 1].replace("'", "").isalpha():
                    numString.append(str(var_list[command_[i]]))
                else:
                    numString.append(str(var_list[command_[i]]))
                    string_to_return += digitResult(numString, lineNum)
            else:
                string_to_return += var_list[command_[i]].replace("'", "")

        # print a string
        elif command_[i][0] == "'" and command_[i][len(command_[i]) - 1] == "'":
            string_to_return += command_[i].replace("'", "")

        # prints a numeric value or result of a numeric equation
        elif command_[i].isdigit() or command_[i] in operators:
            if i + 1 >= len(command_):
                numString.append(str(command_[i]))
                string_to_return += digitResult(numString, lineNum)
            elif not command_[i + 1].replace("'", "").isalpha():
                numString.append(str(command_[i]))
            else:
                numString.append(str(command_[i]))
                string_to_return += digitResult(numString, lineNum)

        # returns a error message
        else:
            return f"ERROR -x-{command_[i]}-x- NOT DEFINED ON LINE NUMBER:- " + lineNum

    return string_to_return


# Takes in mathematical expressions and converts them into on result
# TODO ask Dhruv to add error messages
def digitResult(numbers, lineNum):
    x = len(numbers)
    if x == 1:
        ans = numbers[0]
    elif x % 2 == 0:
        ans = f"ERROR INVALID EXPRESSION ON LINE NUMBER:- " + lineNum
    else:
        expression_list = ['/', '*', '+', '-']
        for expression in expression_list:
            while expression in numbers:
                a = numbers.index(expression)
                val = eval('float(numbers[a - 1])' + expression.replace("\'", "") + 'float(numbers[a + 1])')
                numbers[a - 1] = str(val)
                numbers.pop(a + 1)
                numbers.pop(a)
        ans = numbers[0]
    return ans


# ----------------X-------------------X-------------- PROCESSING OUTPUT COMMANDS ---------X---------------X------------/

# --------------------------------------------------- DEFINE VARIABLES ------------------------------------------------/

# Define variables
# format:
# <variable name>_ = <value>
var_list = {}


def defineVariable(command_, lineNum):
    if command_[1] == "=":
        var_list[command_[0]] = ""
        operators = ['+', '-', '/', '*']
        string_to_return = ""
        numString = []
        for i in range(2, len(command_)):
            # Check is variable already exists
            if command_[i] in var_list:
                if var_list[command_[i]].isdigit() or var_list[command_[i]] in operators:
                    if i + 1 >= len(command_):
                        numString.append(str(var_list[command_[i]]))
                        var_list[command_[0]] += digitResult(numString, lineNum)
                    elif not command_[i + 1].replace("'", "").isalpha():
                        numString.append(str(var_list[command_[i]]))
                    else:
                        numString.append(str(var_list[command_[i]]))
                        var_list[command_[0]] += digitResult(numString, lineNum)
                else:
                    var_list[command_[0]] += var_list[command_[i]].replace("'", "")

            # Check is given value is a string
            elif command_[i][0] == "'" and command_[i][len(command_[i]) - 1] == "'":
                var_list[command_[0]] += command_[i]

            # Checks if the given value is numeric
            elif command_[i].isdigit() or command_[i] in operators:
                if i + 1 >= len(command_):
                    numString.append(str(command_[i]))
                    var_list[command_[0]] += digitResult(numString, lineNum)
                elif not command_[i + 1].replace("'", "").isalpha():
                    numString.append(str(command_[i]))
                else:
                    numString.append(str(command_[i]))
                    var_list[command_[0]] += digitResult(numString, lineNum)
            else:
                return f"ERROR -x- {command_[2]} -x- NOT DEFINED ON LINE NUMBER:- " + lineNum
        return ""
    else:
        return "ERROR MISSING ARRGUMENT (' = ') ON LINE NUMBER:- " + lineNum


# ----------------X-------------------X-------------- DEFINE VARIABLES -------------------X---------------X------------/

# --------------------------------------------------- MYSQL COMMANDS --------------------------------------------------/

# Connect to the mysql server
# format:
# ~/ '<host>' '<user>' '<password>'

connection = False


def mysql_connection(command_, lineNum):
    try:
        global mydb
        mydb = mysql.connector.connect(
            host=command_[1].replace("'", ""),
            user=command_[2].replace("'", ""),
            password=command_[3].replace("'", "")
        )
        global connection
        connection = True
        return "~ Connected to " + command_[1].replace("'", "")

    except:
        return "ERROR INCORRECT DATA ON LINE NUMBER:- " + lineNum


# Command the mysql server
# format:
# ~ '<mysql command>'

def mysql_commands(command_, lineNum):
    # Process the user entered command and execute it in MySQL
    mycursor = mydb.cursor()

    mysql_command_unprocessed = command_[0:len(command_)]

    mysql_command = ""
    for words in mysql_command_unprocessed[1: len(mysql_command_unprocessed)]:
        if words not in var_list:
            mysql_command += words + " "
        else:
            mysql_command += var_list[words] + " "
    mysql_command = mysql_command[0: len(mysql_command) - 1]

    mysql_command = mysql_command.replace("'", "")

    mycursor.execute(mysql_command)

    # Return/Print the output or a appropriate message
    if mysql_command[0:4].lower() == "show" or mysql_command[0:6].lower() == "select":
        returning_File = []
        for data in mycursor:
            returning_File.append(data)
        return returning_File
    else:
        mydb.commit()
        return ["~ " + mysql_command]


# ----------------X-------------------X-------------- MYSQL COMMANDS -------------------X-----------------X------------/

# --------------------------------------------------- FOR LOOPS -------------------------------------------------------/

# For Loops
# format;
# for <variable name> (<start>, <end>, <by how much>) {
#   <code>
#   <code>
#   <code>
# }

def for_loop(loopCommand, loopInfo, lineNum):
    if len(loopCommand) != 4 or loopCommand[3] != "{":
        return "ERROR: UNIDENTIFIED ERROR ON LINE NUMBER:- " + str(lineNum)

    # defining the parameters of the loop
    parameters = loopCommand[2].replace("(", "").replace(")", "").replace(" ", "").split(",")
    for i in range(0, len(parameters)):
        try:
            parameters[i] = int(parameters[i])
        except:
            return "ERROR INAPPROPRIATE ARGUMENT ON LINE NUMBER:- " + str(lineNum)
    if len(parameters) != 3:
        return "ERROR MISSING ARGUMENT ON LINE NUMBER:- " + str(lineNum)

    # The loop
    for comNum in range(parameters[0], parameters[1], parameters[2]):
        var_list[loopCommand[1]] = str(comNum)
        for setLineNum in range(0, len(loopInfo)):
            main_iteration(loopInfo, setLineNum)
    return ""


# ----------------X-------------------X-------------- FOR LOOPS --------------------------X---------------X------------/

# --------------------------------------------------- IF STATEMENTS ---------------------------------------------------/

# For Loops
# format;
# for <variable name> (<start>, <end>, <by how much>) {
#   <code>
#   <code>
#   <code>
# }

def if_statements(ifCommand, ifInfo, lineNum):
    # process the if statements and get the relational data
    relation_arguments = []
    for ifLoop in ifCommand:
        relation_arguments.append([])
        if ifLoop[0] != "else":
            for ifArgs in range(1, 4):
                ifArg = ifLoop[ifArgs].replace("(", "").replace(")", "")
                if ifArg in var_list:
                    lenArg = len(relation_arguments)
                    relation_arguments[lenArg-1].append(var_list[ifArg])
                else:
                    lenArg = len(relation_arguments)
                    relation_arguments[lenArg-1].append(ifArg)
        else:
            lenArg = len(relation_arguments)
            relation_arguments[lenArg - 1].append("else")

    # Run the if statements after check if the given conditions are true or not
    if relationResult(relation_arguments[0][0], relation_arguments[0][1], relation_arguments[0][2]):
        for setLineNum in range(0, len(ifInfo[0])):
            main_iteration(ifInfo[0], setLineNum)
    else:
        exitComm = False
        for i in range(1, len(relation_arguments)):
            if relation_arguments[i] != ["else"] and relationResult(relation_arguments[i][0], relation_arguments[i][1], relation_arguments[i][2]):
                for setLineNum in range(0, len(ifInfo[i])):
                    main_iteration(ifInfo[i], setLineNum)
                exitComm = False
                break
            elif relation_arguments[i] == ["else"]:
                exitComm = True
        if exitComm == True:
            for setLineNum in range(0, len(ifInfo[i])):
                main_iteration(ifInfo[i], setLineNum)

    # TODO add the error messages
    return ""


def relationResult(a,b,c):
    if a == '56':
        return True
    else:
        return False


# ----------------X-------------------X-------------- IF STATEMENTS ----------------------X---------------X------------/

# --------------------------------------------------- EXECUTING COMMANDS ----------------------------------------------/

# required variables
loopCommand = ''
loopInfo = []
ifCommand = []
ifInfo = [[]]
ifTemp = 0


def main_iteration(commands_, command):
    # Execution of the for loop. I don't know that how the FUCK it works, I just know that I was messing with some code
    # and it started working, so please don't touch this part of the code
    if commands_[command][0] == "for":
        global loopCommand
        loopCommand = commands_[command]
        global loopInfo
        loopInfo = []
    elif loopCommand != '' and commands_[command][0] != "}":
        loopInfo.append(commands_[command])
    elif loopCommand != '' and commands_[command][0] == "}":
        xFact = loopCommand
        loopCommand = ''
        message = for_loop(xFact, loopInfo, command + 1)
        loopInfo = []
        if message[0:5] == "ERROR":
            print(message)
            return False
        command += 1
    elif commands_[command][0] == '}':
        pass

    # Execution of if else stratments
    # TODO ADD THE ERROR MESSAGES
    elif commands_[command][0] == "if":
        global ifCommand
        global ifInfo
        global ifTemp
        ifCommand.append(commands_[command])
        ifInfo = [[]]
        ifTemp = 0
    elif len(ifCommand) != 0 and commands_[command][0] != "}}":
        if commands_[command - 1][0] == "},":
            ifCommand.append(commands_[command])
            ifInfo.append([])
            ifTemp += 1
        elif commands_[command][0] != "},":
            ifInfo[ifTemp].append(commands_[command])
    elif ifCommand != '' and commands_[command][0] == "}}":
        ifCommand_ = ifCommand
        ifCommand = []
        if_statements(ifCommand_, ifInfo, command)
        # Here the ifCommand_ contains the if and else statement and the ifInfo contains the code to put in statement
        ifInfo = [[]]
        ifTemp = 0

    # Execution of the show command
    elif commands_[command][0] == "show":
        print()
        print(showCommand(commands_[command], str(command + 1)))
        print()
        if showCommand(commands_[command], str(command + 1))[0:5] == "ERROR":
            return False

    # Deceleration of new variables
    elif commands_[command][0][len(commands_[command][0]) - 1] == "_":
        var_content = defineVariable(commands_[command], str(command + 1))
        if var_content != "":
            print()
            print(var_content)
            print()
            return False

    # MYSQL commands
    elif commands_[command][0][0] == "~":
        # Connects to the mysql sever
        if len(commands_[command][0]) == 2:
            if commands_[command][0][1] == "/":
                message = mysql_connection(commands_[command], str(command + 1))
                print()
                print(message)
                print()
                if message[0:5] == "ERROR":
                    return False
        # Execute mysql commands after connecting to the server
        else:
            if connection:
                print()
                for statments in mysql_commands(commands_[command], str(command + 1)):
                    print(statments)
                print()
            else:
                print()
                print("ERROR NOT CONNECTED TO MySQL SEVER")
                return False

    else:
        print(f"ERROR -x- {commands_[command][0]} -x- COMMAND NOT FOUND!!")
        return False


# final loop that executes all the commands
for command in range(len(commands_)):
    if main_iteration(commands_, command) == False:
        break
