class Car():
    def __init__(self,model,band):
        self.model = model
        self.band = band
    def start(self):
        pass
    def stop(self):
        pass
class Home(Car):
    def __init__(self,model,band,name):
        super().__init__(model,band)
        self.name = name
    def start(self):
        print(f'我是{self.name},我的汽车我做主')
    def stop(self):
        print('目的地到了，我们去玩吧')
class Taxi(Car):
    def __init__(self,model,band,company):
        super().__init__(model,band)
        self.company = company
    def start(self):
        print('乘客您好！')
        print(f'我是{self.company}的，我的车牌是{self.band}，您要去哪里？')
    def stop(self):
        print('目的地到了，请您付款下车，欢迎下次乘坐')
home=Home('che','A5555','武大郎')
home.start()
home.stop()
taxi=Taxi('che','A8888','长城出租车公司')
taxi.start()
taxi.stop()
