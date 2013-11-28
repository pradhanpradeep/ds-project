import json
import time
import csv
import traceback
import codecs, cStringIO
#
#
# http://docs.python.org/2/library/csv.html#examples
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        #! *** one addition here, to bypass the ints / floats from encoding
        self.writer.writerow([ s if not isinstance(s, (str, unicode)) else s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
def print_time(func):
    """
    -------------------------------------------------------------------
    This is a simple decorator function to print the start and end time
      of a function it decorates.
    -------------------------------------------------------------------
    """
    def wrapper_func(*args):
        print '------- start time - (%s) -----'%(time.asctime())
        func(*args)
        print '------- finish time - (%s) -----'%(time.asctime())
    return wrapper_func

def flatten_dict(d):
    """
    lists are converted to strings with comma separated
    dicts are converted to strings too with the structure intact
    """
    final = d.copy()    
    for key, val in d.items():
        if isinstance(val, (list, tuple)):
            final[key] = ",".join(val)
        if isinstance(val, dict):
            temp = []
            for k,v in val.items():
                temp.append(str(k)+"++"+str(v))
            final[key] = ",".join(temp)
    return final
        
@print_time
def convert_json_csv(filename):
    """
    """
    json_list = []
    with open(filename, 'rb') as input_file:
        for line in input_file:            
            line = line.strip('\r\n').strip('\n')
            json_obj = json.loads(line, encoding="utf-8")
            json_list.append(json_obj)            

    header = json_list[0].keys() #! keys from the first dict obj
    f = open("%s.csv"%(filename), 'wb')
    UnicodeWriter(f).writerow(header)
    bad_ones = 0
    for json_obj in json_list:
        o = flatten_dict(json_obj)
        try:
            UnicodeWriter(f).writerow([o[column] for column in header])
        except:
            bad_ones += 1
            continue
    f.close()

    print '-- total no of json objects = %i '%(len(json_list))
    print '-- no of bad ones = %i '%(bad_ones)
                

if __name__ == '__main__':
    convert_json_csv('yelp_training_set/yelp_training_set_business.json')
    convert_json_csv('yelp_training_set/yelp_training_set_review.json')
    convert_json_csv('yelp_training_set/yelp_training_set_user.json')
    convert_json_csv('yelp_training_set/yelp_training_set_checkin.json')
