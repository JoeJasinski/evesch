class Message(object):
    title = ""
    text = ""
    links = []

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text
        self.links = []

    class Links(object):
        link = ""
        name = ""
        def __init__(self,name,link):
            self.link = link
            self.name = name
        
        def __unicode__(self):
            return self.name
        
        def __str__(self):
            return self.name
            
    def addlink(self, name, link):
        self.links.append(self.Links(name,link))
    
    def __unicode__(self):
        return "%s - %s"%(self.title, self.text) 
    
    def __str__(self):
        return "%s - %s"%(self.title, self.text) 

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    return "%X" % n

def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

#print "hex2dec('FF') =", hex2dec('FF') # 255

def text_vs_bg(bgcolor):
    if not bgcolor:
        bgcolor='FFFFFF'
    red1 = hex2dec(bgcolor[0:2]) 
    green1 = hex2dec(bgcolor[2:4]) 
    blue1 = hex2dec(bgcolor[4:6]) 
    
    red2 = hex2dec('0') 
    green2 = hex2dec('0') 
    blue2 = hex2dec('0') 
    
    LR1 = (red1/255)**2.2
    LG1 = (green1/255)**2.2
    LB1 = (blue1/255)**2.2
    
    LR2 = (red2/255)**2.2
    LG2 = (green2/255)**2.2
    LB2 = (blue2/255)**2.2
    
    L1 = .2126*LR1 + .7152*LG1 + .0722*LB1
    L2  = .2126*LR2 + .7152*LG2 + .0722*LB2
    
    lum_ratio = (L1+.05) / (L2+.05)
    
    if lum_ratio < 5:
        return 'ffffff'
    else:
        return '000000'


class ePage(object):
    next = None
    curr = None
    prev = None
    num_pages = 0
    pages = None

    def __init__(self, page):
        self.curr = page
    
    def set_pages(self, pages):
        self.pages = pages
        self.num_pages = pages.num_pages
        self.validate()
        
    def validate(self):
        self.next = self.curr + 1
        self.prev = self.curr - 1
        if self.prev <= 0:
            self.prev = False
        if self.next > self.num_pages:
            self.next = False
        if self.curr <= 0:
            self.curr = 1
        if self.curr > self.num_pages:
            self.curr = self.num_pages
            
    def current_page(self):
        return self.pages.page(self.curr)