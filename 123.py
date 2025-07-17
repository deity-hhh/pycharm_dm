class Student():
    def __init__(self,name,age,gender,score):
        self.name=name
        self.age=age
        self.gender=gender
        self.score=score
    def info(self):
        print(self.name,self.age,self.gender,self.score)
lst=[]
for i in range(1,6):
    s=input(f'请输入第{i}位学生信息')
    lst2=s.split('#')
    stu=Student(lst2[0],lst2[1],lst2[2],lst2[3])
    lst.append(stu)

for item in lst:
    item.info()
