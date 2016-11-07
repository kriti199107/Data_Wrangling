
# coding: utf-8

# # MAP AREA
# 
# I selected the Benguluru city in India. The reason behind the choice is that I am from India and my favorite city is Benguluru. Also, my sister and my friends are settled there. So, it would be interesting to explore the city further more!
# I went to map zen  to extract the data using the link https://mapzen.com/data/metro-extracts/. Benguluru city data is available under India.

#  # EXPLORING THE DATA:

# ## Extracting small data set
# I spent quite sometime in understanding and exploring the data. Since the data file is really big (609 MB), I ran my codes first on a small sample of the dataset. I used the following code(shared on the project details) to extract a small data set.

# In[ ]:

#!/usr/bin/env python

from pprint import pprint
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "bengaluru_india.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            pprint(ET.tostring(element, encoding='utf-8'))
        

    output.write('</osm>')


# ## Finding the number of tags in the file
# This is helpul to understand the different type as well as the count of the tags in the data set

# In[1]:

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags= {}
    for event, element in ET.iterparse(filename):
        if element.tag not in tags.keys():
            tags[element.tag]=1
        else:
            tags[element.tag]+=1
    return tags


# In[3]:

filename="bengaluru_india.osm"


# In[4]:

print count_tags(filename)


# ## Finding problematic characters in key attribute of tags
# This is helpul to clean the data and get rid of any problemetic characters in the key attribute of the data set.

# In[24]:

import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

keys={'lower': 0,
      'lower_colon': 0, 
      'other': 0,
      'problemchars': 0}
def key_type(filename,keys):
    for event, element in ET.iterparse(filename):
        if element.tag == "tag":
            if lower.search(element.attrib['k']):
                keys["lower"] += 1
                
            elif lower_colon.search(element.attrib['k']):
                keys["lower_colon"] += 1
                    
            elif problemchars.search(element.attrib['k']):
                keys["problemchars"] += 1
        
            else:
                keys["other"] += 1
    return keys

print key_type(filename,keys)


# In[20]:

print keys['problemchars']


# In[29]:

print problem_characters


# ## A code to find out number of identical users 
# A single user could have made multiple entries in the data. This code gives us an idea of how many unique users have worked on the dataset.

# In[8]:

#code to count the number of unique users

def number_of_users(filename):
    users = set()
    elements=["node" , "way","relation"]
    for event, element in ET.iterparse(filename):
        if element.tag in elements:
            user_id=element.attrib["uid"]
            if user_id not in users:
                users.add(user_id)
        

    return len(users)




# In[9]:

filename="sample.osm" # run for a sample of the dataset first


# In[10]:

print number_of_users(filename)


# In[31]:

filename="bengaluru_india.osm" # run for the whole dataset of bengaluru city


# In[14]:

print number_of_users(filename)


#  # Problem Encountered
# The user name in the data is inconsistent. Some use their first name, such as user="PlaneMad". Some use their full name such as user="Gururaja Upadhyaya" while some just use some username like user="user_634020".

# ## Correcting Problem: Code to generalize username as one word
# In order to generalize the user name the following code was written. This code splits the given name and then combines all the words using '_'. 

# In[42]:

#code to change the username such that it is more general- a one word
#users_name_modified = set()
def modifying_user_name(filename,users_name_modified):
   
    elements=["node" , "way","relation"]
    for event, element in ET.iterparse(filename):
        if element.tag in elements:
            user_name=element.attrib["user"]
            user_name_list=user_name.split(' ')
            number_words=len(user_name_list)
            first_word=user_name_list[0]
            for i in range(1,number_words):
                user_name_modified=first_word+'_'+user_name_list[i]
                first_word=user_name_modified
                users_name_modified.append(user_name_modified)
    return users_name_modified
                    
                
                
                
                

        

   


# # Problem Encountered
# After running the code I noticed that same user has spelled the user name in different ways. Example,
# 'Pradeep_B_V', 'Pradeep_B', 'Pradeep_B_V'

# ## Correcting Problem: Code to check if the a unique user has spelled the name in the same way. If not, the necessary correction should be made

# In[ ]:

import xml.etree.cElementTree as ET
def modified_user_name(name):
    user_name_list=name.split(' ')
    number_words=len(user_name_list)
    first_word=user_name_list[0]
    for i in range(1,number_words):
        user_name_modified=first_word+'_'+user_name_list[i]
        first_word=user_name_modified

    return first_word
   


# In[ ]:

users={}
ulist=[]
def correct_user_name(filename,users,list):
    elements=["node" , "way","relation"]
    for event, element in ET.iterparse(filename):
        if element.tag in elements:
            user_id=element.attrib["uid"]
            user_name=element.attrib["user"]
            user_name_corrected=modified_user_name(user_name)
            if user_id not in users.keys():
                users[user_id]=user_name_corrected
                element.attrib["user"]=user_name_corrected
                ulist.append(user_name_corrected)
            else:
                user_id in users.keys() and (user_name_corrected not in users.values())
                user_name_changed=users[user_id]
                element.attrib["user"]=user_name_changed
                ulist.append(user_name_changed)
                
    return ulist


# In[ ]:

filename="sample.osm"
print correct_user_name(filename,users)


#  # Exploring the data further

# ## Code to check the different type of keys present in the dataset

# In[1]:

# A code to check what all type of keys are present in different tags
import xml.etree.cElementTree as ET
keys_category={}
def key_type_category(filename,keys_category):
    for event, element in ET.iterparse(filename):
        if element.tag == "tag":
            key=element.attrib['k']
            if key not in keys_category.keys():
                keys_category[key]=element.attrib['v']
                
    return keys_category


# ## Code to count the number of times a key is present in the dataset

# In[11]:

# A code to count the number of keys

keys_count={}
def key_type_count(filename):
    for event, element in ET.iterparse(filename):
        if element.tag == "tag":
            key=element.attrib['k']
            if key not in keys_count.keys():
                keys_count[key]=1
            else:
                keys_count[key]+=1
                
                
    return keys_count


# In[14]:

filename="bengaluru_india.osm" # run for the whole dataset of bengaluru city
print key_type_count(filename)


#  # CONVERTING THE DATASET TO CSV FILE 
#  The code used in the case study was modified to account for the change in the user name to make it more genrelazied

# In[ ]:

import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH ="bengaluru_india.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def correct_k(k):
    index=k.find(':')
    typ=k[:index]
    k=k[index+1:]    
    return k,typ
def modified_user_name(name):
    user_name_list=name.split(' ')
    number_words=len(user_name_list)
    first_word=user_name_list[0]
    for i in range(1,number_words):
        user_name_modified=first_word+'_'+user_name_list[i]
        first_word=user_name_modified

    return first_word

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag=='node':
        for i in node_attr_fields:
            if i=='user':
                user_name=element.attrib[i]
                user_name_corrected=modified_user_name(user_name)
                node_attribs[i]=user_name_corrected
            else:    
                node_attribs[i]=element.attrib[i]
            
    if element.tag=='way':
        for i in way_attr_fields:
            if i=='user':
                user_name=element.attrib[i]
                user_name_corrected=modified_user_name(user_name)
                way_attribs[i]=user_name_corrected
            else:    
                way_attribs[i]=element.attrib[i]
        
    for tag in element.iter("tag"):
        dic={}
        attributes=tag.attrib
        if problem_chars.search(tag.attrib['k']):
            continue
        
        if element.tag=='node':
            dic['id']=node_attribs['id']
        else:
            dic['id']=way_attribs['id']
        
        dic['value'] = attributes['v']

        colon_k=LOWER_COLON.search(tag.attrib['k'])
        if colon_k:
            print colon_k.group(0)
            print tag.attrib['k']
            dic['key'],dic['type']=correct_k(tag.attrib['k'])
        else:
            dic['key']=attributes['k']
            dic['type']='regular'
        
        
        #print dic
        tags.append(dic)
    
    if element.tag=='way':
        position=0
        for nd in element.iter("nd"):
            way_node_dic={}
            way_node_dic['id']=way_attribs['id']
            way_node_dic['node_id']=nd.attrib['ref']
            way_node_dic['position']=position
            position = position + 1
            way_nodes.append(way_node_dic)
             
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)


# # SQL QUERIES

# ## Coverting the nodes_tag.csv file into table called nodes_tag

# In[ ]:

import sqlite3
import csv
from pprint import pprint


# In[ ]:

sqlite_file = 'mydb.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)


# In[ ]:

# Get a cursor object
cur = conn.cursor()


# In[ ]:

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
# commit the changes
conn.commit()


# In[ ]:

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


# In[ ]:

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('nodes_tags.csv','rb') as fin:
    dr = UnicodeDictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]


# In[ ]:

# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()


# In[ ]:

cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)


# ## Converting all the csv files to SQL tables
# Similar codes as above were written and run to convert all the csv files to tables in SQL. Such as nodes.csv was converted to nodes5 and ways.csv was converted to ways5

# ## Query for counting number of nodes
# 

# In[ ]:

import sqlite3
import csv
from pprint import pprint
sqlite_file = 'mydb.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)
# Get a cursor object
cur = conn.cursor()
cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)


#  ANSWER: 2843099

# ## Query for counting number of ways

# In[ ]:

QUERY = "SELECT COUNT(*) FROM ways5;"
cur.execute(QUERY)
count=cur.fetchall()
print count


# Answer: 652702

# ## Verification
# our values for the number of nodes and ways is correct as we ran the code for the number of tags before and we got the following results: {'node': 2843099, 'nd': 3527513, 'bounds': 1, 'member': 5086, 'tag': 776670, 'relation': 939, 'way': 652702, 'osm': 1}

# ## Query for counting number of unique users in tags nodes and ways

# In[ ]:

QUERY = "SELECT COUNT(DISTINCT(e.uid))FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;"
cur.execute(QUERY)
count=cur.fetchall()
print count


# Answer: 1439

# ## Query for finding top 10 contributing users

# In[ ]:

QUERY = "SELECT e.user, COUNT(*) as num FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e GROUP BY e.user ORDER BY num DESC LIMIT 10;"
cur.execute(QUERY)
result=cur.fetchall()
print result


# Answer: [(u'jasvinderkaur', 102703), (u'akhilsai', 95506), (u'saikumar', 92071), (u'premkumar', 91840), (u'shekarn', 80449), (u'PlaneMad', 76776), (u'vamshikrishna', 73810), (u'himalay', 71049), (u'himabindhu', 70142), (u'sdivya', 68493)]

# # Additional suggestions for improving and analyzing the data.

# Area of Improvement: 
# Since I encountered the problem regarding the inconsistency in user name, I think that is one area that can be improved. 
# 
# How?
# The users can be asked to create an account using a username that has some specifications. For example, in my school we have usernames consisting of 6 characters. For example my ID is krs437. Here, the first three letters represent my initials while the last three numbers are random digits so that the whole combination is a unique to every user. 

# # Discussion about the benefits as well as some anticipated problems in implementing the improvement.

# Implementing the above mentioned improvement would ensure both the consistency as well as uniqueness. However, it is not a very easy task because this would require a lot of cleaning and correcting the data that is already stored in the database. It would be exhausting!
