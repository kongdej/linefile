import os
import pymupdf
import re
import sqlite3
import pytz 
import zeep
from datetime import datetime

src_directory ='/workspace/documents'
dest_directory = '/workspace/public'

def filter_thai_english_numbers(text):
    # Regular expression pattern to match Thai, English, or numbers
    pattern = re.compile(r'[ก-๙A-Za-z0-9 /.]+')
    
    # Use the pattern to find all matches in the text
    matches = pattern.findall(text)
    
    # Join the matches to form the filtered text
    filtered_text = ''.join(matches)
    
    return filtered_text

#add documents
con = sqlite3.connect("../database.db")
cur = con.cursor()
# Creating table
table = """ 
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        filepath TEXT,
        created VARCHAR(25) NOT NULL
    ); 
    """
cur.execute(table)

for root, dirs, files in os.walk(src_directory):
    for file in files:
        if file.endswith('pdf') or  file.endswith('PDF'):
            src_path = os.path.join(root, file)
            title = file.replace('.pdf','').replace('.PDF','')
            hashfile = str(hash(src_path))[1:16]+'.PDF'
            dest_path = dest_directory + root.replace(src_directory,'') + '/' + hashfile
            print(src_path)

            doc = pymupdf.open(src_path) # open a document
            text = ''
            for page in doc: # iterate the document pages
                text += page.get_text() # get plain text (is in UTF-8)
            
            text = text.replace('..','').replace(' .',' ')
            text = filter_thai_english_numbers(text)
            text = " ".join(text.split())
            
            print(text) # write text of page
            print('----------------------------------------------------')
           
            # insert into table
            sql = 'INSERT INTO documents (title, content, filepath, created)VALUES(?,?,?,?)'
            val = (title,text, hashfile, datetime.now(pytz.timezone('Asia/Bangkok')))
            cur.execute(sql, val)
            con.commit()
            
            
            
            #check if table not exists create documents table
            #check if document not exists insert data into documents table
                #extract pdf content
                #insert into table documents
                #copy to public directory  
    

print ('Total: ', len(files))

