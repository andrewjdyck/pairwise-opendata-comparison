#!/usr/bin/python
import sys
import p
sys.path.append('/home/anddyc1/py_libs/')

# import modules
import web, pycurl, csv, random
import simplejson as json

# urls for the app
urls = ( '/', 'index',
        '/add', 'add',
        '/datasets', 'datasets',
        '/stats', 'stats')

# the web.py application
app = web.application(urls, globals())

# templates folder rendering
render = web.template.render('templates/')

# iriscouch db
odsk_url = 'http://' + p.u + ':' + p.p + '@odsk.iriscouch.com/pw_odata'


# read dataset
def read_datasets():
    reader = csv.DictReader(open('./static/data/datasets.csv', 'r'))
    lstData = [ row for row in reader ]
    random.shuffle(lstData)
    return lstData


class index:
    def GET(self):
        lstData = read_datasets()
        web.header('Content-Type', 'text/html')
        return render.index(lstData)


class add:
    def POST(self):
        user_data = web.input()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, odsk_url)
        ch.setopt(pycurl.POST, 1)
        ch.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
        ch.setopt(pycurl.POSTFIELDS, json.dumps(user_data))
        ch.perform()


class datasets:
    def GET(self):
        lstData = read_datasets()
        web.header('Content-Type', 'application/json')
        return json.dumps(lstData[:2])


class stats:
    def GET(self):
        web.header('Content-Type', 'text/html')
        return render.stats("hello")



if __name__ == "__main__":
    app.run()
else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, 
addr)


