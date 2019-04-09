num = int(input("what is the number?: "))
primes = []
for i in range(1,num):
    prime = True
    for x in range(2,i-1):
        if i%x == 0:
            print(i, ' is a NOT a prime')
            prime = False
            break
    if prime:
        print(i, ' IS a prime')
        primes.append(i)
        
print('the numbers that are prime are: ',primes)    

