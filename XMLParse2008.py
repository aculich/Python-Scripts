import sys
sys.path.append( '.' )
from patXML import SQLPatent
from patXML import XMLPatent
from patXML import uniasc
from fwork  import *
import os, datetime, re

#flder='test'
flder = '/var/share/patentdata/patents/2010'
t1 = datetime.datetime.now()

#get a listing of all files within the directory that follow the naming pattern
files = [x for x in os.listdir(flder)
         #if re.match(r"ip[a-z]{2}[0-9]{6,8}[.]xml", x, re.I)!=None]
         #if re.match(r"ipg\d{6}.one.xml", x, re.I)!=None]
         if re.match(r"ipg\d{6}.xml", x, re.I)!=None]
print "Total files: %d" % (len(files))

#sys.exit()

tables = ["assignee", "citation", "class", "inventor", "patent", "patdesc", "lawyer", "sciref", "usreldoc"]
total_count = 0
total_patents = 0
for filenum, filename in enumerate(files):
    print " > Regular Expression: %s" % filename
    XMLs = re.findall(
            r"""
                ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
                .*?
                [<][/]us[-]patent[-]grant[>])    #and here is the end tag
             """,
            open(flder+"/"+files[filenum]).read(), re.I + re.S + re.X)
    print "   - Total Patents: %d" % (len(XMLs))

    xmllist = []
    count = 0
    patents = 0
    for i, x in enumerate(XMLs):
        try:
            xmllist.append(XMLPatent(x))
            patents += 1
        except Exception as inst:
            print type(inst)
            print "  - Error: %s (%d)  %s" % (filename, i, x[175:200])
            count += 1
    print "   - number of patents:", len(xmllist), datetime.datetime.now()-t1
    print "   - number of errors: " ,count
    total_count += count
    total_patents += patents
    for table in tables:
        SQLPatent().dbBuild(q=SQLPatent().tblBuild(xmllist, tbl=table), tbl=table, week=filename)
    print "   -", datetime.datetime.now()-t1
    print "   - total errors: ", total_count
    print "   - total patents: ", total_patents

for table in tables:
    SQLPatent().dbFinal(tbl=table)
