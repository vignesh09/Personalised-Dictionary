
import requests
import webbrowser
from bs4 import BeautifulSoup
import sqlite3


from flask import Flask,request
from flask import render_template


def getmeaning(word):
    try:
        url='http://www.dictionary.com/browse/'+word
        #print (url)
        r = requests.get(url)
        soup=BeautifulSoup(r.content,'lxml')

        pos = soup.findAll("header", { "class" : "luna-data-header" })


        meanings = soup.findAll("div", { "class" : "def-content" })

        #print (pos[0].text)

        #print (meanings[0].text.strip())
        #if(pos.count>=0):

        webpage(word,pos[0].text,meanings[0].text.strip())
        return 1
        
    except IndexError:
        webpage(word,"","Enter the correct spelling and try again or link the link below to search in google");
        return 0

    
def getmeaning_all(word):
    url='http://www.dictionary.com/browse/'+word
    #print (url)
    r = requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')

    pos = soup.findAll("header", { "class" : "luna-data-header" })


    meanings = soup.findAll("div", { "class" : "def-content" })
   
    Html_file= open("templates/webpage_allwords","a")
    string="""<div class="col s12 m3">
          <div class="card blue-grey darken-1   box-shadow">
            <div class="card-content white-text">
              <span class="card-title">"""+word+"""</span>
              <p>"""+pos[0].text.strip()+"""</p><p>"""+meanings[0].text.strip()+"""</p>
            </div>
            <div class="card-action">
              <a href="https://www.google.co.in/?q="""+word+"""">search in google</a>
               <a href="/delete/"""+word+"""""><i class="material-icons">delete</i></a>
            
            </div>
          </div>
        </div>"""
    #print (string)
    Html_file.write(string)
    Html_file.close()
    

    
    
#create the webpage

def webpage(word,pos,meaning,webpage="templates/webpage-words"):
    Html_file=open('templates/header.html',"r")
    lines=Html_file.readlines()
    Html_file_out=open(webpage,"w")
    for line in lines:
        Html_file_out.write(line)
        #print (line)
    Html_file.close()
    Html_file_out.close()
    Html_file= open("templates/webpage-words","a")
    string="""<div class="col s12 m3">
          <div class="card blue-grey darken-1   box-shadow">
            <div class="card-content white-text">
              <span class="card-title">"""+word+"""</span>
              <p>"""+pos+"""</p><p>"""+meaning+"""</p>
            </div>
            <div class="card-action">
              <a href="https://www.google.co.in/?q="""+word+"""">search in google</a>
            </div>
          </div>
        </div>"""
    #print (string)
    Html_file.write(string)
    Html_file.close()
    Html_file=open('templates/footer.html',"r")
    lines=Html_file.readlines()
    Html_file_out=open("templates/webpage-words","a")
    for line in lines:
        Html_file_out.write(line)
        #print (line)
    Html_file.close()
    Html_file_out.close()
    


    
#db connection and insert into table words
def insertword(word):
    conn=sqlite3.connect("words_")

    c=conn.cursor()

    c.execute('''create table if not exists words_ (word text)''')
    if word!=" ":
    	c.execute('insert into words_ values (?)',(word,))

    conn.commit()
    #set the header

    Html_file=open('templates/header.html',"r")
    lines=Html_file.readlines()
    Html_file_out=open("templates/webpage_allwords","w")
    for line in lines:
        Html_file_out.write(line)
        print (line)
    Html_file.close()
    Html_file_out.close()
    index=1
    #get words from the db
    for row in c.execute("select word from words_"):
    	getmeaning_all(row[0])
    	if index%4==0:
	    	Html_file_out=open("templates/webpage_allwords","a")
	    	Html_file_out.write(""" </div><div class="row">  """)
	    	Html_file_out.close()
    	index=index+1

	    
	    
    #set the footer
    Html_file=open('templates/footer.html',"r")
    lines=Html_file.readlines()
    Html_file_out=open("templates/webpage_allwords","a")
    for line in lines:
        Html_file_out.write(line)
        #print (line)
    Html_file.close()
    Html_file_out.close()
   
    conn.close()
    
#get input from the user
#webbrowser.open('D:\\Unicode_Python_Session_1\\webpage-words.html')
app = Flask(__name__)

@app.route("/entry")
def entry():
	insertword(" ")
	return render_template('entry.html')

@app.route("/hello", methods=['GET','POST'])
def hello():
	word=""
	if(request.method=='POST'):
		word=request.form.get('word')
		res=getmeaning(word)
		if(res):
		    insertword(word)

		return render_template('webpage-words')

@app.route("/allwords")
def allwords():
	return render_template('webpage_allwords')


@app.route("/delete/<word>")
def delete(word):
	conn=sqlite3.connect("words_")

	c=conn.cursor()

	#c.execute('''create table words (word text)''')
	test='delete from words_ where word="'+word+'"'
	
	c.execute(test)

	conn.commit()
	insertword(" ")
	
	return render_template('webpage_allwords')


	
if __name__ == '__main__':
    app.debug = True
    app.run()
