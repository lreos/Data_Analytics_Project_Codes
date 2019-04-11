question = True
while question:

    str = input('Good day. What is your problem? Enter your response here or Q to quit:')
    str1 = str.split(' ')
    str2 = ''
    for x in str1:
        if x.lower() == 'i':
            str2 += 'You'
        elif x.lower() == 'my':
            str2 += 'Your'
        else:
            str2 += x
        str2 += ' '
    print(str2)

    if str.lower() == "great" or str.lower() == "q":
        question = False
        
print('End')
