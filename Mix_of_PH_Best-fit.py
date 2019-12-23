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


def best_checking_the_priority_heuristic(width, rectangles):
    wh = 0

    answer = [None] * len(rectangles)
    who_is_left = rectangles
    for idx, r in enumerate(who_is_left):
        if r[0] > r[1]:
            who_is_left[idx][0], who_is_left[idx][1] = who_is_left[idx][1], who_is_left[idx][0]
    sorted_indices = sorted(range(len(who_is_left)), key=lambda x: -who_is_left[x][wh])
    x, y, w, h, H = 0, 0, 0, 0, 0
    while sorted_indices:
        idx = sorted_indices.pop(0)
        r = who_is_left[idx]
        if r[1] > width:
            answer[idx] = (x, y, r[0], r[1])
            x, y, w, h, H = r[0], H, width - r[0], r[1], H + r[1]
        else:
            answer[idx] = (x, y, r[1], r[0])
            x, y, w, h, H = r[1], H, width - r[1], r[0], H + r[0]
        helping_function(x, y, w, h, 1, who_is_left, sorted_indices, answer)
        x, y = 0, H

    return H, answer


def helping_function(x, y, w, h, D, who_is_left, indices, answer):
    checking_the_priority = 6
    for idx in indices:
        for j in range(0, D + 1):
            if checking_the_priority > 1 and who_is_left[idx][(0 + j) % 2] == w and who_is_left[idx][(1 + j) % 2] == h:
                checking_the_priority, orientation, best = 1, j, idx
                break
            elif checking_the_priority > 2 and who_is_left[idx][(0 + j) % 2] == w and who_is_left[idx][(1 + j) % 2] < h:
                checking_the_priority, orientation, best = 2, j, idx
            elif checking_the_priority > 3 and who_is_left[idx][(0 + j) % 2] < w and who_is_left[idx][(1 + j) % 2] == h:
                checking_the_priority, orientation, best = 3, j, idx
            elif checking_the_priority > 4 and who_is_left[idx][(0 + j) % 2] < w and who_is_left[idx][(1 + j) % 2] < h:
                checking_the_priority, orientation, best = 4, j, idx
            elif checking_the_priority > 5:
                checking_the_priority, orientation, best = 5, j, idx
    if checking_the_priority < 5:
        if orientation == 0:
            omega, d = who_is_left[best][0], who_is_left[best][1]
        else:
            omega, d = who_is_left[best][1], who_is_left[best][0]
        answer[best] = (x, y, omega, d)
        indices.remove(best)
        if checking_the_priority == 2:
            helping_function(x, y + d, w, h - d, D, who_is_left, indices, answer)
        elif checking_the_priority == 3:
            helping_function(x + omega, y, w - omega, h, D, who_is_left, indices, answer)
        elif checking_the_priority == 4:
            min_w = 10000000000000
            min_h = 10000000000000
            for idx in indices:
                min_w = min(min_w, who_is_left[idx][0])
                min_h = min(min_h, who_is_left[idx][1])

            min_w = min(min_h, min_w)
            min_h = min_w
            if w - omega < min_w:
                helping_function(x, y + d, w, h - d, D, who_is_left, indices, answer)
            elif h - d < min_h:
                helping_function(x + omega, y, w - omega, h, D, who_is_left, indices, answer)
            elif omega < min_w:
                helping_function(x + omega, y, w - omega, d, D, who_is_left, indices, answer)
                helping_function(x, y + d, w, h - d, D, who_is_left, indices, answer)
            else:
                helping_function(x, y + d, omega, h - d, D, who_is_left, indices, answer)
                helping_function(x + omega, y, w - omega, h, D, who_is_left, indices, answer)


def main():
    boxes = []
    boxes_best_fit = []
    answer_matrix = []
    length, width = map(int, input().split("\t"))
    number_of_cars = int(input())

    for i in range(number_of_cars):
        w, h = map(int, input().split("\t"))
        boxes.append([w, h])
        if h > w:
            h, w = w, h
        boxes_best_fit.append([w * h, w, h, i + 1])

    for i in range(length):
        temp = []
        for j in range(width):
            temp.append([length - i, 0])
        answer_matrix.append(temp)

    cavab = best_fit_search(boxes_best_fit, answer_matrix)

    height, rectangles = best_checking_the_priority_heuristic(width, boxes)
    if height == length:
        n = height
        m = width
        a = [0] * n
        for i in range(n):
            a[i] = [0] * m

        for it in range(len(rectangles)):
            for i in range(rectangles[it][1], rectangles[it][1] + rectangles[it][3]):
                for j in range(rectangles[it][0], rectangles[it][0] + rectangles[it][2]):
                    a[i][j] = it + 1

        for i in range(n):
            for j in range(m):
                if j != m - 1:
                    print(a[i][j], end='\t')
                else:
                    print(a[i][j])
            print(end='\n')
    else:
        height, rectangles = best_checking_the_priority_heuristic(length, boxes)
        if height == width:
            n = height
            m = length
            a = [0] * n
            for i in range(n):
                a[i] = [0] * m

            for it in range(len(rectangles)):
                for i in range(rectangles[it][1], rectangles[it][1] + rectangles[it][3]):
                    for j in range(rectangles[it][0], rectangles[it][0] + rectangles[it][2]):
                        a[i][j] = it + 1

            for i in range(m):
                for j in range(n):
                    if j != n - 1:
                        print(a[j][i], end='\t')
                    else:
                        print(a[j][i])
                print(end='\n')
        else:
            for i in range(len(cavab)):
                for j in range(len(cavab[i])):
                    if j != len(cavab[i]) - 1:
                        print(cavab[i][j][1], end='\t')
                    else:
                        print(cavab[i][j][1])
                print(end='\n')


if __name__ == "__main__":
    main()
