import sys

def read_file_lines(file_name):
    with open(file_name) as file:
        lines = file.read().splitlines()
    return lines


def display_data(data):
    for line in data:
        print(''.join(line))


def was_mine_pased(data):
    for n0 in range(len(data)):
        for n1 in range(len(data[0])):
            if data[n0][n1] == '*':
                return True
    return False


def are_mines_clear(data):
    for n0 in range(len(data)):
        for n1 in range(len(data[0])):
            if data[n0][n1] != '.':
                return False
    return True


def count_mines(data):
    count = 0
    for n0 in range(len(data)):
        for n1 in range(len(data[0])):
            if data[n0][n1] != '.':
                count += 1
    return count


def count_volleys(script):
    count = 0
    for n0 in range(len(script)):
        # print "n0", script[n0]
        for n1 in range(len(script[n0])):
            # print "n1", script[n0][n1]
            if script[n0][n1] in volleys:
                # print "found volley", script[n0][n1]
                count += 1
    return count


def count_moves(script):
    count = 0
    for n0 in range(len(script)):
        # all_blanks = True
        # print "n0", script[n0]
        for n1 in range(len(script[n0])):
            # print "n1", script[n0][n1]
            if script[n0][n1] in moves:
                count += 1
                # all_blanks = False
                # print "found move", script[n0][n1]
        # if all_blanks:
        #     count += 1
    return count


def raise_mines(data):
    for n0 in range(len(data)):
        for n1 in range(len(data[0])):
            if data[n0][n1] != '.':
                if data[n0][n1] == 'A':
                    c = 'z'
                elif data[n0][n1] in ['a', '*']:
                    c = '*'
                else:
                    c = chr(ord(data[n0][n1]) - 1)
                data[n0][n1] = c


def min_mat(data):
    bd = True
    while bd:
        bd = False

        if len(data) >= 3:
            new_line = ['.'] * len(data[0])
            if data[0] == new_line and data[-1] == new_line:
                data.pop(0)
                data.pop(-1)
                bd = True

        if len(data[0]) >= 3:
            west = [l[0] == '.' for l in data]
            is_west_empty = False not in west
            east = [l[-1] == '.' for l in data]
            is_east_empty = False not in east

            if is_west_empty and is_east_empty:
                for n in range(len(data)):
                    data[n].pop(0)
                    data[n].pop(-1)
                bd = True


def north(data):
    data.insert(0, ['.'] * len(data[0]))
    data.insert(0, ['.'] * len(data[0]))


def south(data):
    data.append(['.'] * len(data[0]))
    data.append(['.'] * len(data[0]))


def east(data):
    for n in range(len(data)):
        data[n].append('.')
        data[n].append('.')


def west(data):
    for n in range(len(data)):
        data[n].insert(0, '.')
        data[n].insert(0, '.')


def alpha(data):
    sx = int(len(data[0]) / 2)
    sy = int(len(data) / 2)
    if len(data[0]) >= 3 and len(data) >= 3:
        data[sy - 1][sx - 1] = '.'
        data[sy - 1][sx + 1] = '.'
        data[sy + 1][sx - 1] = '.'
        data[sy + 1][sx + 1] = '.'


def beta(data):
    sx = int(len(data[0]) / 2)
    sy = int(len(data) / 2)
    if len(data[0]) >= 3 and len(data) >= 3:
        data[sy - 1][sx + 0] = '.'
        data[sy + 0][sx - 1] = '.'
        data[sy + 1][sx + 0] = '.'
        data[sy + 0][sx + 1] = '.'


def gamma(data):
    sx = int(len(data[0]) / 2)
    sy = int(len(data) / 2)
    # print( data[sy][sx] )
    if len(data[0]) >= 3:
        data[sy][sx - 1] = '.'
        data[sy][sx + 1] = '.'
    data[sy][sx + 0] = '.'


def delta(data):
    sx = int(len(data[0]) / 2)
    sy = int(len(data) / 2)
    if len(data) >= 3:
        data[sy - 1][sx] = '.'
        data[sy + 0][sx] = '.'
        data[sy + 1][sx] = '.'


# List of valid commands
moves = ['north', 'south', 'east', 'west']
volleys = ['alpha', 'beta', 'gamma', 'delta']


def apply_cmd(data, cmd):
    # verify command is not a code injection attack
    if cmd in moves + volleys:
        cmd_str = cmd + '(data)'
        eval(cmd_str)


if __name__ == '__main__':
    # print "Arguments", sys.argv[1:]
    # fieldFile = sys.argv[1]
    # scriptFile = sys.argv[2]

    # for testing purposes only, comment when done
    fieldFile  = 'examples/test'+str(sys.argv[1])+'.field'
    scriptFile  = 'examples/test'+str(sys.argv[1])+'.script'
    

    # READING IN FIELD AND COMMANDS
    # data = read_file_lines(fieldFile)
    # script = read_file_lines(scriptFile)
    f = open(fieldFile, "r")
    data=[]
    for line in f:
        strippedLine = line.strip()
        listVersion = list(strippedLine)
        data.append(listVersion)

    s = open(scriptFile, "r")
    script = []
    for line in s:
        strippedLine = line.strip()
        wordsSplit = strippedLine.split()
        script.append(wordsSplit)

    # print "field:", data
    # print "commands:", script

    #COUNTING ALL COMMANDS, MINES, AND VOLLEYS
    n_mines = count_mines(data)
    n_volleys = count_volleys(script)
    n_moves = count_moves(script)
    # print n_mines, "mines" , n_volleys, "volleys", n_moves, "moves"

    #CALCULATING RESULT
    for step in range(len(script)):
        print("\nStep %s\n" % (step + 1))
        display_data(data)
        print("\n%s\n" % ' '.join(script[step]))
        for cmd in script[step]:
            # print "appying cmd", cmd
            apply_cmd(data, cmd)
            min_mat(data)
        raise_mines(data)
        display_data(data)

        b_mp = was_mine_pased(data)
        b_mc = are_mines_clear(data)

        if b_mp or b_mc:
            break

    # print "\n\ncalculating score"
    if b_mc:
        if step < len(script) - 1:
            score = 1
        else:
            mine_score = n_mines * 10
            # print "volley score is min of 5*n_mines", 5*n_mines, "and 5*n_volleys", 5*n_volleys
            volley_score = min(5*n_mines, 5*n_volleys)
            # print "move score is min of 3*n_mines", 3*n_mines, "and 2*n_moves", 2*n_moves
            move_score = min(3*n_mines, 2*n_moves)
            score = mine_score - volley_score - move_score
            # print score, "=", mine_score, "-", volley_score, "-", move_score
    else:
        score = 0

    if score == 0:
        print('\nfail (0)')
    else:
        print('\npass (%d)' % score)
