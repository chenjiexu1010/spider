# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import random
import math

l = []
for i in range(10):
    l.append(random.randint(0, 100))
print(l)


def bulling_sort(collection):
    for i in range(collection.__len__() - 1):
        for j in range(collection.__len__() - 1 - i):
            if collection[j] > collection[j + 1]:
                temp = collection[j + 1]
                collection[j + 1] = collection[j]
                collection[j] = temp
    print(collection)


def selection_sort(collection):
    for i in range(collection.__len__() - 1):
        minIndex = i
        # j = i + 1
        for j in range(collection.__len__() - i - 1):
            j = j + 1 + i
            if collection[j] < collection[minIndex]:
                minIndex = j
        temp = collection[i]
        collection[i] = collection[minIndex]
        collection[minIndex] = temp
    print(collection)


def insertion_sort(collection):
    preIndex, current = 0, 0
    for i in range(collection.__len__()):
        preIndex = i - 1
        current = collection[i]
        while preIndex >= 0 and collection[preIndex] > current:
            collection[preIndex + 1] = collection[preIndex]
            preIndex -= 1
        collection[preIndex + 1] = current
    print(collection)


def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            while i >= gap and arr[i] < arr[i - gap]:
                arr[i], arr[i - gap] = arr[i - gap], arr[i]
                i -= gap
                print(arr)
        gap //= 2
    print(arr)


def merge(a, b):
    c = []
    h = j = 0
    while j < len(a) and h < len(b):
        if a[j] < b[h]:
            c.append(a[j])
            j += 1
        else:
            c.append(b[h])
            h += 1

    if j == len(a):
        for i in b[h:]:
            c.append(i)
    else:
        for i in a[j:]:
            c.append(i)

    return c


def merge_sort(lists):
    if len(lists) <= 1:
        return lists
    middle = len(lists) / 2
    left = merge_sort(lists[:middle])
    right = merge_sort(lists[middle:])
    return merge(left, right)


# print(math.floor(10))
# bulling_sort(l)
# selection_sort(l)
# insertion_sort(l)
# shell_sort(l)
merge_sort(l)
