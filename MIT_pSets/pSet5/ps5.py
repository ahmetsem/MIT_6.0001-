# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:
import feedparser
from feedparser import *
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime,timezone
import pytz
import re

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory (object):
    def __init__(self,guid,title,description,link,pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger (Trigger):
    def __init__(self,phrase):
        self.phrase=phrase

    def evaluate(self, story):
        return self.is_pharese_in(story)

    def is_pharese_in(self,text):

        if type(self) is TitleTrigger:
            phr = self.title_phrase.lower()
        elif type(self) is DescriptionTrigger:
            phr = self.descrp_phrase.lower()

        new_text=""
        flag=True
        for item in text:
            if item in string.punctuation and flag:
                new_text +=" "
                flag=False
            if item not in string.punctuation:
                new_text += item.lower()
                flag=True

        index=0
        count=0
        phr = re.sub(' +', ' ', phr)
        new_text = re.sub(' +', ' ', new_text)

        for i in range(len(new_text)):
            if new_text[i] == phr[index]:
                count+=1
                index+=1
            else:
                index=0
                count=0
                
            if count == len(phr):
                if i<len(new_text)-1:
                    if new_text[i+1]==" ":
                        return True
                    else:
                        index=0
                        count=0
                else:
                    return True
        return False


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self,title_phrase):
        self.title_phrase=title_phrase

    def evaluate(self, story):
        return self.is_pharese_in(story.get_title())



# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self,descrp_phrase):
        self.descrp_phrase=descrp_phrase

    def evaluate(self, story):
        return self.is_pharese_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self,time_string):
        self.time=(datetime.strptime(time_string,"%d %b %Y %H:%M:%S"))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger (TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self,time)

    def evaluate(self, item):
        time=self.time.replace(tzinfo=pytz.UTC)
        time2=item.pubdate.replace(tzinfo=pytz.UTC)
        if time > time2:
            return True
        return False

class AfterTrigger (TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self,time)

    def evaluate(self, item):
        time = self.time.replace(tzinfo=pytz.UTC)
        time2 = item.pubdate.replace(tzinfo=pytz.UTC)
        if time < time2:
            return True
        return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger (Trigger):
    def __init__(self,trigger):
        self.trigger=trigger

    def evaluate(self,item):
        if not self.trigger.evaluate(item):
            return True
        return False

# Problem 8
# TODO: AndTrigger
class AndTrigger (Trigger):
    def __init__(self,t1,t2):
        self.t1=t1
        self.t2=t2

    def evaluate(self,item1):
        if self.t1.evaluate(item1) and self.t2.evaluate(item1):
            return True
        return False



# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def evaluate(self,item):
        if self.t1.evaluate(item) or self.t2.evaluate(item):
            return True
        return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    lst=[]
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                lst.append(story)

    return lst



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_dict={}
    trigger_list=[]

    for i in range(len(lines)):
        trigger_name = ""
        trigger_type = ""
        trigger_object = ""
        check_name = True
        check_type = False
        check_obje = False
        and_flag=True
        or_flag=True
        add_flag=True

        for j in range(len(lines[i])):
            if check_name:
                trigger_name+=lines[i][j]

            if lines[i][j] == "," or check_type:
                trigger_type+=lines[i][j]
                check_name=False
                check_type=True
                if trigger_type[-1:]==',' and len(trigger_type)>1:
                    check_type=False
                    check_obje=True
                    trigger_name = trigger_name[:-1]
                    trigger_type = trigger_type[1:-1]

            if trigger_name=="ADD"and add_flag:
                add_values=lines[i][j:]
                add_flag=False
                for item in trigger_dict:
                    if item in add_values:
                        trigger_list.append(trigger_dict[item])

            if check_obje:
                if lines[i][j]!=",":
                    trigger_object+=lines[i][j]

                if trigger_type=="TITLE" and j==len(lines[i])-1:

                    trigger_dict[trigger_name]=TitleTrigger(trigger_object)

                elif trigger_type=="DESCRIPTION"and j==len(lines[i])-1:
                    trigger_dict[trigger_name] = DescriptionTrigger(trigger_object)

                elif trigger_type == "AFTER"and j==len(lines[i])-1:

                    trigger_dict[trigger_name] = AfterTrigger(trigger_object)

                elif trigger_type == "BEFORE"and j==len(lines[i])-1:
                    trigger_dict[trigger_name] = BeforeTrigger(trigger_object)

                elif trigger_type == "NOT"and j==len(lines[i])-1:
                    trigger_dict[trigger_name] = NotTrigger(trigger_object)

                elif trigger_type == "AND" and and_flag:
                    trigger_object=lines[i][j:]
                    and_flag=False
                    and_triggers=[]
                    for item in trigger_dict:
                        if item in trigger_object:
                            and_triggers.append(trigger_dict[item])
                    trigger_dict[trigger_name]=AndTrigger(and_triggers[0],and_triggers[1])

                elif trigger_type == "OR" and or_flag:
                    trigger_object = lines[i][j:]
                    or_flag = False
                    or_triggers = []
                    for item in trigger_dict:
                        if item in trigger_object:
                            or_triggers.append(trigger_dict[item])

                    trigger_dict[trigger_name] = OrTrigger(or_triggers[0], or_triggers[1])

    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("Prince Harry")
        # t2 = DescriptionTrigger("Samsung")
        # t3 = DescriptionTrigger("Galaxy")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

