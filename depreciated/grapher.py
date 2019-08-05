import matplotlib.pyplot as plt

### works only on two column csvs, thus is now depreciated ###

def display(some_list_x, some_list_y):
    plt.scatter(some_list_x, some_list_y, s=1)
    plt.draw()
    plt.pause(100000)
    plt.clf()

def tupleize_2(string):
    string = string.split(',')
    out = []
    for element in string:
        out.append(float(element))

    return tuple(out)

def get_point(line):
    point_1 = ''
    index = 0
    for char in line:
        if char != ',':
            point_1 = point_1 + char
            index += 1
        else:
            break

    point_2 = ''
    count = 0
    for char in line:
        if char != ',' and count >= index:
            point_2 = point_2 + char
            count += 1
        elif char == ',' and count > index:
            break
        else:
            count += 1

    point = point_1 + ',' + point_2
    return point

list_x = []
list_y = []

with open("out.csv", 'r') as csv:
    skip = 0
    for line in csv:
        if skip == 0:
            skip += 1
        else:
            point = get_point(line)

            #print(point)
            #print(type(point))

            fin_point = tupleize_2(point)
            print(fin_point)
            list_x.append(fin_point[0])
            list_y.append(fin_point[1])
    csv.close()

print(list_x)
print(list_y)

display(list_x, list_y)
