employee = [[001,'Mary',15,40],[002,'John',22,25],[003,'Bob',35,4],[004,'Mel',43,62],[005,'Jen',17,33],
[006,'Sue',29,45],[007,'Ken',40,36],[008,'Dave',20,17],[009,'Beth',37,37],[010,'Ray',16.50,80]]

for i in employee:
	if i[3]<= 40:
		pay = i[2]*i[3]
		print(i[1],pay)
	else
		overtime = i[3]-40
		pay = (i[2]*40)+ (i[2]*1.5*overtime
		print(pay)
