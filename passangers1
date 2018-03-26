# -*- encoding: utf-8 -*-


def process():
    
    try:
        train1 = int(input('Input number of railway carriages(for 1st train):'))
        A = []
        for i in range(train1):
            print('Input number of people in',i+1,'carriage:')
            a = int(input())
            A.append(a)
        train2 = int(input('Input number of railway carriages(for 2nd train):'))
        B = []
        for i in range(train2):
            print('Input number of people in',i+1,'carriage:')
            b = int(input())
            B.append(b)
            
        car, num = map(int,input('Input number of train & number of carriage \
for walk: ').split(' '))
        walk = int(input('Walk: '))
        if car == 1:
            A[num - 1] -= 1
            A[num + walk - 1] += 1
        elif car == 2:
            B[num - 1] -= 1
            B[num + walk - 1] += 1
        sw = int(input('Input number of train for switch: '))

        switch = int(input('Switch: '))
        if sw == 1:
            B += A[len(A) - switch:]
            A = A[:len(A) - switch]        
        elif sw == 2:
            A += B[len(B) - switch:]
            B = B[:len(B) - switch]
        tr, vn = map(int,input('Input number of train & number of carriage \
to find out nuber of passengers: ').split(' '))
        if tr == 1:
            res = A[vn - 1]
        elif tr == 2:
            res = B[vn - 1]
        return res
    except:
        return -1
