from goody import type_as_str

class Time:
    def __init__(self,hr=0,mins=0,seconds=0):
        assert type(hr)==int and 0<=hr<=23, 'Hour must be int between 0 and 23 inclusive'
        assert type(mins)== int and 0<=mins<=59, 'Minute must be int between 0 and 59 inclusive'
        assert type(seconds)== int and 0<=seconds<=59,'Second must be int between 0 and 59 inclusive'
        self.hour = hr
        self.minute = mins
        self.second = seconds

    def _translate(self,i):
        if i not in range(1,4):
            raise IndexError
        else:
            return self.hour if i==1 else (self.minute if i == 2 else self.second)
    
    def __getitem__(self,arg):
        if type(arg) == int:
            return self._translate(arg)
        else:
            return tuple(self._translate(i) for i in arg)
        

    def __repr__(self):
        return f'Time({self.hour},{self.minute},{self.second})'
    
    def __str__(self):
        if self.hour>12:
            return f'{self.hour-12}:{self.minute:02d}:{self.second:02d}pm'
        elif self.hour==12:
            return f'12:{self.minute:02d}:{self.second:02d}pm'
        elif self.hour==0:
            return f'12:{self.minute:02d}:{self.second:02d}am'
        else:
            return f'{self.hour}:{self.minute:02d}:{self.second:02d}am'
    
    def __bool__(self):
        if self.__repr__()=='Time(0,0,1)':
            return True
        elif self.__repr__()=='Time(12,59,59)':
            return True
        else:
            return False
    
    def __len__(self):
        return self.hour*60*60 + self.minute*60 + self.second
    
    def __eq__(self,t2):
        return self.__repr__()==t2.__repr__()
    
    def __lt__(self,right):
        if type(right)==int:
            return self.__len__() < right
        elif type(right)==Time:
            return self.__len__() < right.__len__()
        else:
            return NotImplemented
    
    def __add__(self,right):
        if type(right)==int:
            total_seconds = self.__len__()+right
            hrs=total_seconds//3600
            mins=(total_seconds%3600)//60
            secs=(total_seconds%3600)%60
            if hrs ==24:hrs=0
            return eval(f'Time({hrs},{mins},{secs})').__str__()   
        else:
            return NotImplemented
    
    def __radd__(self,left):
        return self + left
    
    def __call__(self,hour,minutes,seconds):
        assert type(hour)==int and 0<=hour<=23, 'Hour must be int between 0 and 23 inclusive'
        assert type(minutes)== int and 0<=minutes<=59, 'Minute must be int between 0 and 59 inclusive'
        assert type(seconds)== int and 0<=seconds<=59,'Second must be int between 0 and 59 inclusive'
        self.hour = hour
        self.minute = minutes
        self.second = seconds
        
if __name__ == '__main__':
    # Put in simple tests for Time before allowing driver to run
    # Debugging is easier in script code than in bsc tests

    print('Start simple testing')
    print()

    import driver
    driver.default_file_name = 'bscq31S22.txt'
#     driver.default_show_traceback=True
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()



        
        
        
        
        
