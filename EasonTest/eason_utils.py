from contextlib import contextmanager
import logging

@contextmanager
def mute_logging():
    import logging
    logging.disable()
    try:
        yield
    finally:
        logging.disable(0)
        
class DataFrameBatchIterator:
    def __init__(self, dataframe, batch_size):
        self.df = dataframe
        self.index = 0
        self.batch_size = batch_size

    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.df):
            self.index += self.batch_size
            return self.df[self.index - self.batch_size: self.index].copy()
        else:
            raise StopIteration

# Timezone and log
from datetime import datetime,tzinfo,timedelta

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name

d = datetime.now(tz=Zone(8,False,'GMT'))
now_time_string = d.strftime("%m_%d_%H:%M:%S")
log_file_name = f"{now_time_string}.log"
print(f"{log_file_name=}")
def lprint(text, *args, **kwargs):
    texts = [text] + list(args)
    texts = map(lambda x: str(x), texts)
    text = ' '.join(texts)
    print(text)
    with open(f'./log/{log_file_name}', 'a') as f:
        f.write(datetime.now(tz=Zone(8,False,'GMT')).strftime("[%m_%d_%H:%M:%S] \t") + text + "\n")
        
def change_log_file_name(text):
    global log_file_name
    log_file_name = text