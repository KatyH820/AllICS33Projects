from collections import defaultdict
import re


class TrackHistory:
    def __init__(self):
        self._tracking_dict = defaultdict(list)

    def __setattr__(self, name, value):
        if '_prev' in name:
            raise NameError(
                "New attributes should not containing the string '_prev'")
        self.__dict__[name] = value
        if name != '_tracking_dict':
            self._tracking_dict[name].append(value)

    def __getattr__(self, name):
        m = re.search(r'(.+)_prev(\d+)?', name)
        if m == None or m.group(1) not in self._tracking_dict:
            raise NameError("Name not found")
        index = -2 if (m.group(2) is None) else -1 if (int(m.group(2))==0) else -int(m.group(2))-1
        if abs(index)>len(self._tracking_dict[m.group(1)]):
            return None
        return self._tracking_dict[m.group(1)][index]


    def __getitem__(self, index):
        if index > 0: raise IndexError("The index cannot be positive")
        return dict({k:(None if abs(index-1)>len(self._tracking_dict[k]) else self._tracking_dict[k][index-1]) for k in self._tracking_dict})



if __name__ == '__main__':
    # Put in simple tests for TrackHistory before allowing driver to run
    # Debugging is easier in script code than in bsc tests
    print('Start simple testing')
    print()
    import driver
    driver.default_file_name = 'bscq32S22.txt'
#     driver.default_show_traceback=True
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
