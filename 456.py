class Instrument():
    def make_sound(self):
        pass
class Erhu(Instrument):
    def make_sound(self):
        print('二胡在弹奏')
class Piano(Instrument):
    def make_sound(self):
        print('钢琴在演奏')
class Violin(Instrument):
    def make_sound(self):
        print('小提琴在演奏')
erhu=Erhu()
piano=Piano()
violin=Violin()
def play(obj):
    obj.make_sound()
play(erhu)
play(piano)
play(violin)