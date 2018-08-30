

L = [104, 13, 12, 7]


#插入排序：直接插入排序，希尔排序
#选择排序：简单选择排序，堆排序
#交换排序：冒泡排序，快速排序
#归并排序
#基数排序

'''
insert_sort:
    假定有一个有序序列A(从小到大排列) 和 无序序列B, 每次从无序序列B中选择一个数 插入到有序序列A中 并使得A仍然有序，直到A和B组成的序列有序
'''
def insert_sort(lst):
    for i in range(1, len(lst), 1):
        temp = lst[i]
        j =  i
        while j > 0 and temp < lst[j - 1]:
            lst[j] = lst[j - 1]
            j = j - 1
        lst[j] = temp

    return lst
'''
shell_sort:
    分组进行直接插入排序，每次按照 n/2进行分组，在分组内进行直接插入排序

    如：3, 4, 1, 6, 2, 9, 7, 0, 8, 5
    第一次分组：10/2 = 5， (3 9), (4 7), (1 0), (6 8), (2 5) = (3, 4, 0, 6, 2, 9, 7, 1, 8, 5)
    第二次分组：5/2 = 2,  (3 0 2 7 8), (4 6 9 1 5) = (0, 1, 2, 4, 3, 5, 7, 6, 8, 9)
    第三次分组：2/2 = 1, (0, 1, 2, 4, 3, 5, 7, 6, 8, 9)进行直接插入排序
'''
def shell_sort(lst):
    n = len(lst)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n, 1):
            temp = lst[i]
            j = i
            while j > 0 and temp < lst[j - gap]:
                lst[j] = lst[j - gap]
                j = j - gap
            lst[j] = temp
        gap = gap // 2

    return lst
'''
一组数，每趟比较 选择一个最值沉到最底下，
如[3, 4, 1, 6, 2, 9, 7, 0, 8, 5]， 10个数只需要比较9趟，每趟比较出一个最值
每次两两相邻的数进行比较
'''
def bubble_sort(lst):
    for i in range(0, len(lst) - 1, 1):#比较的趟数
        for j in range(0, len(lst) - i - 1, 1):#每一趟需要比较的次数
            if lst[j + 1] < lst[j]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

    return lst
'''
一组数[3, 4, 1, 6, 2, 9, 7, 0, 8, 5]
选择基准x=3, i=0, j=9,j--直到找到比基准3小的数替换3所在位置上的值，然后i++直到找到比基准大的值替换到j的位置。
0, 4, 1, 6, 2, 9, 7, (3), 8, 5 [从右往左找，直到找到比基准3小的数去替换3位置上的数， 0被挖坑]
0, (3), 1, 6, 2, 9, 7, 4, 8, 5 [从左往右找，直到找到比基准3大的数去填充原0的坑位]
0, 2, 1, 6, (3), 9, 7, 4, 8, 5 [从右往左找，直到找到比基准3小的数去替换3位置上的数， 2被挖坑]
0, 2, 1, 3, 6, 9, 7, 4, 8, 5   [从左往右找，直到找到比基准3大的数去填充原2的坑位]
一轮排序得到[0, 2, 1, 3, 6, 9, 7, 4, 8, 5] 得到以3的左边都是小于3的数列， 3的右边都是大于3的数列
继续对数列(0, 2, 1)及 数列（6, 9, 7, 4, 8, 5）按照如上的步骤重复，直到整个序列都有序
'''
def quick_sort(lst, l, r):
    if l < r:
        i, j = l, r
        x = lst[l]
        while i != j:
            while i != j and lst[j] > x:
                j = j - 1
            if i != j:
                lst[i] = lst[j]
            while i != j and lst[i] < x:
                i = i + 1
            if i != j:
                lst[j] = lst[i]
        lst[i] = x
        quick_sort(lst, l, i - 1)
        quick_sort(lst, i + 1, r)

    return lst

'''
选择排序与插入排序类似，都是由一个有序区 + 一个无序区，所不同的是，直接插入是每次从无序区中选择第一个插入到有序区并使得有序区仍然有序，
而选择排序是，从无序区中选择一个最小值直接插入到有序区的尾部
'''
def select_sort(lst):
    n = len(lst)
    for i in range(0, n - 1, 1):#有序数列范围从1到n-1,
        for j in range(i + 1, n, 1):#从有序数列的剩余范围为无序数列，
            if lst[j] < lst[i]:
                lst[i], lst[j] = lst[j], lst[i]

    return lst

def heap_adjust(lst, start, end):#start:父结点
    lchild = 2 * start + 1 #下标从0开始
    rchild = 2 * start + 2
    if lchild < end and lst[lchild] > lst[start]:
        maxIndex = lchild
    else:
        maxIndex = start
    if rchild < end and lst[rchild] > lst[maxIndex]:
        maxIndex = rchild
    if maxIndex != start:#原父节点不是最大结点，则与最大结点交换
        lst[start], lst[maxIndex] = lst[maxIndex], lst[start]
        heap_adjust(lst, maxIndex, end)#此句执行的作用是，原子结点被替换到父节点， 新子节点的分支可能需要调整为最大堆
    return lst

def build_max_heap(lst):
    for i in range(len(lst) // 2 - 1, -1, -1): #下标从0开始
        heap_adjust(lst, i, len(lst))
    return lst

'''
堆排序： 升序数列用最大堆(二叉树)， 最大堆的根节点是数列的最大值， 用根结点和最后一个叶子结点去交换， 得到新的二叉树（结点数减1）继续调整为最大堆，重复如上步骤。
'''
def heap_sort(lst):
    build_max_heap(lst)
    n = len(lst)
    for i in range(len(lst) - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]#用根节点去替换最后一个叶结点
        n = n - 1
        heap_adjust(lst, 0, n)
    return lst

'''
基数排序（桶排序）：
L = [13, 104, 12, 7, 9]
分为10个桶（0-9）
1.先以个位上的数进行桶排序得到[[], [], [12], [13], [104], [], [], [7], [], [9]]
合并桶(12,13,104,7,9)
2.在序列(12,13,104,7,9)的基础上，以十位上的数字进行桶排序得到[[104, 7, 9], [12, 13], [], [], [], [], [], [], [], []]
合并桶(104,7,9,12,13)
3.在序列(104,7,9,12,13)的基础上，以百位上的数字进行桶排序得到[[7, 9, 12, 13], [104], [], [], [], [], [], [], [], []]
合并桶（7, 9, 12, 13, 104）
'''
def radix_sort(lst):#L = [13, 104, 12, 7, 9]
    k = len(str(max(lst)))
    for i in range(k):
        s = [[] for i in range(10)]
        for j in lst:
            s[j // (10 ** i) % 10].append(j)
        lst = [b for a in s for b in a]#合并桶
    return lst
        # lst1 = []
        # for a in s:
        #     for b in a:
        #         lst1.append(b)
        # lst = lst1

def merge(left, right):
    i, j = 0, 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    num = len(lst) // 2
    left = merge_sort(lst[:num])
    right = merge_sort(lst[num:])
    return merge(left, right)

if __name__ == '__main__':

    # ret = heap_sort(L)
    ret = merge_sort(L)
    print(ret)
