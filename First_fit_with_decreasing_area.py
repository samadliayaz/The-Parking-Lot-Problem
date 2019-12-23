def check_the_point(x, y, w, h, answer):
    for j in range(x, x + w):
        if j >= len(answer[0]):
            return False
        if answer[y][j][0] < h or answer[y][j][1] != 0:
            return False
    return True


def fill_the_point(x, y, w, h, ind, answer):
    for j in range(x, x + w):
        for k in range(y-1, 0, -1):
            if answer[k][j][0] != 0:
                answer[k][j][0] = y - k
            else:
                break

    for i in range(y, y + h):
        for j in range(x, x + w):
            answer[i][j][0] = 0
            answer[i][j][1] = ind


def best_fit_search(cars, answer):
    cars.sort(reverse=True)

    for i in range(len(cars)):
        checking = False
        for j in range(len(answer)):
            for k in range(len(answer[j])):

                if check_the_point(k, j, cars[i][1], cars[i][2], answer):
                    fill_the_point(k, j, cars[i][1], cars[i][2], cars[i][3], answer)
                    checking = True
                    break
            if checking:
                break
        if not checking:
            for j in range(len(answer)):
                for k in range(len(answer[j])):
                    if check_the_point(k, j, cars[i][2], cars[i][1], answer):
                        fill_the_point(k, j, cars[i][2], cars[i][1], cars[i][3], answer)
                        checking = True
                        break
                if checking:
                    break
    return answer

def main():
    boxes = []
    result_matrix = []
    length, width = map(int, input().split("\t"))
    number_of_cars = int(input())

    for i in range(number_of_cars):
        w, h = map(int, input().split("\t"))
        if h > w:
            h, w = w, h
        boxes.append([w * h, w, h, i + 1])

    for i in range(length):
        temp = []
        for j in range(width):
            temp.append([length - i, 0])
        result_matrix.append(temp)

    cavab = best_fit_search(boxes, result_matrix)

    for i in range(len(cavab)):
        for j in range(len(cavab[i])):
            if j != len(cavab[i]) - 1:
                print(cavab[i][j][1], end='\t')
            else:
                print(cavab[i][j][1])
        print(end='\n')


if __name__ == "__main__":
    main()


