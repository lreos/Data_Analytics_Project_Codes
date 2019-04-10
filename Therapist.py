question = True
while question:
    str = input('Good day. What is your problem? Enter your response here or Q to quit:')
    if str.find('I am'):
        print(str.replace('I am', 'You are'))
    elif str.find('my'):
        print(str.replace('my', 'your'))
    else:
        print(str)
    if str.lower() == "great" or str.lower() == "q":
        question = False

print('End')

