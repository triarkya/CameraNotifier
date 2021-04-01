from dateutil import parser


'''
ctime attribute will be provided within VideoDetector
but same as time.ctime(os.path.getctime("filename"))
- parsed_time: datetime type
'''
class Blacklist:
    def __init__(self, ctime):
        self.blacklisted = False
        self.parsed_time = parser.parse(ctime)
        self.check_if_blacklisted()


    '''
    set blacklisting attributes here:
    - which weekdays or times to skip
    '''
    def check_if_blacklisted(self):
        # skip all saturdays
        if self.parsed_time.weekday() == 5:
            return True

        return False
