def prog():
    print('input number: ')
    a = int(input())
    if a % 2 == 0:
        print('chet!')
    elif a % 2 == 1:
        print('nechet!')
    else:
        print('ERROR!!!!')