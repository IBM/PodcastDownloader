import mysql.connector
import pecan
from flask import Flask, request
import requests as req
from pyPodcastParser import  Podcast
import pycurl

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('PODCASTS_DOWNLOADER_SETTINGS', silent=True)

cnx = mysql.connector.connect(user='root',password='dliu',host='127.0.0.1', database='podcast_downloader')
# Get buffered cursors
curA = cnx.cursor(buffered=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@pecan.expose('json')
@app.route('/customer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def customer():
    name = request.args.get('name','')
    try:
        if request.method == 'GET':
            print 'customer name is :%s' % name
            item = _getcustomer(name)
            if item:
                (id,name)=item
                return app.make_response('The user info is id %s, name %s' % (id,name))
            else:
                return 'object not found', 404
        elif request.method == 'POST':
            print 'in post'
            item = _getcustomer(name)
            if item:
                return 'object already existed', 400
            elif _addcustomer(name):
                return app.make_response('created customer %s' % (name))
            else:
                return 'error happened', 400
        elif request.method == 'DELETE':
            print 'in delete'
            item = _getcustomer(name)
            if item:
                if _deletecustomer(name):
                    return app.make_response('User %s deleted' %name)
                else:
                    return 'error happened', 400
            else:
                return 'object not found', 404
        elif request.method == 'PUT':
            print 'in put'
            oldname = request.args.get('oldname', '')
            item = _getcustomer(oldname)
            if item:
               if _putcustomer(name,oldname):
                  return app.make_response('Updated user %s' %name)
               else:
                   return 'error happened', 400
            else:
                return 'object not found', 404
    except Exception:
        return 'error happened', 400

def _getcustomer(name):
    try:
        print 'in _getcustomer'
        query = "select customerid, name from customer where name = '%s'" % name
        print query
        curA.execute(query)
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None

def _getcustomer_byid(customerid):
    try:
        print 'in _getcustomer by id'
        query = "select customerid, name from customer where customerid = '%s'" % customerid
        print query
        curA.execute(query)
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None


def _addcustomer(name):
    try:
        print 'in _addcustomer'
        query = "insert into customer (name) values ('%s')" %name
        print query
        curA.execute(query)
        cnx.commit()
        return True
    except Exception:
        return False

def _deletecustomer(name):
    try:
        print 'in _deletecustomer'
        query = "delete from customer where name = '%s'" %name
        print query
        curA.execute(query)
        cnx.commit()
        return True
    except Exception:
        return False


def _putcustomer(name,oldname):
    try:
        print 'in _putcustomer'
        query = "update customer set name=('%s') where name=('%s')" %(name,oldname)
        print query
        curA.execute(query)
        item =curA.fetchone()
        print item
        cnx.commit()
        return True
    except Exception:
        return False

@pecan.expose('json')
@app.route('/podcast', methods=['GET', 'POST', 'PUT', 'DELETE'])
def podcast():
    podname = request.args.get('podname')
    try:
        if request.method == 'GET':
            print 'in podcast get'
            item = _getpodcast(podname)
            if item:
                (podid, podname, podurl) = item
                return app.make_response('The podcast info is id %s, podname %s, url %s' % (podid, podname, podurl))
            else:
                return 'object not found', 404
        elif request.method == 'POST':
            print 'in post'
            url = request.args.get('url')
            item = _getpodcast(podname)
            if item:
                return 'object already existed', 400
            elif _addpodcast(podname,url):
                return app.make_response('created podcast %s' % (podname,url))
            else:
                return 'error happened', 400
        elif request.method == 'DELETE':
            item = _getpodcast(podname)
            if item:
                if _deletepodcast(podname):
                    return app.make_response('podcast %s deleted' % podname)
                else:
                    return 'error happened', 400
            else:
                return 'object not found', 404
        elif request.method == 'PUT':
            print 'in put'
            newurl = request.args.get('url')
            item = _getpodcast(podname)
            if item:
                if _putpodcast(podname,newurl):
                    return app.make_response('podcast %s updated' % podname)
                else:
                    return 'error happened', 400
            else:
                return 'object not found', 404
    except Exception:
        return 'bad request', 400

def _getpodcast(podname):
    try:
        print 'in _getpodcast'
        query = "select podid, podname, url from podcast where podname = '%s'" % podname
        print query
        curA.execute(query)
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None

def _getpodcast_byid(podid):
    try:
        print 'in _getpodcast_byid'
        query = "select podid, podname, url from podcast where podid = '%s'" % podid
        print query
        curA.execute(query)
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None

def _addpodcast(podname,url):
    try:
        print 'in _addpodcast'
        query = "insert into podcast (podname,url) values ('%s', '%s')" %(podname,url)
        print query
        curA.execute(query)
        cnx.commit()
        return True
    except Exception:
        return False

def _deletepodcast(podname):
    try:
        print 'in _deletepodcast'
        query = "delete from podcast where podname = '%s'" % podname
        print query
        curA.execute(query)
        cnx.commit()
        return True
    except Exception:
        return False

def _putpodcast(podname,url):
    try:
        print 'in _putcustomer'
        query = "update podcast set url='%s' where podname=('%s')" %(url,podname)
        print query
        curA.execute(query)
        item =curA.fetchone()
        print item
        cnx.commit()
        return True
    except Exception:
        return False

@pecan.expose('json')
@app.route('/sub', methods=['GET', 'POST', 'PUT', 'DELETE'])
def sub():
    customerid = request.args.get('customerid','')
    podid = request.args.get('podid','')
    try:
        if request.method == 'GET':
            print 'in sub get'
            item = _getsub(customerid,podid)
            if item:
                (subid, customerid, podid) = item
                return app.make_response('subid %s, customerid %s, podid %s' %(subid,customerid,podid))
            else:
                return 'object not found', 404
        elif request.method == 'POST':
            print 'in post'
            item = _getsub(customerid,podid)
            if item:
                return 'object already existed', 400
            elif _addsub(customerid, podid):
                return app.make_response('created subscription %s' % (customerid, podid))
            else:
                return 'error happened', 400
        elif request.method == 'DELETE':
            print 'in delete'
            item = _getsub(customerid, podid)
            if item:
                if _deletesub(customerid):
                    return app.make_response('subscription deleted')
                else:
                    return 'error happened', 400
            else:
                return 'object not found', 404
        elif request.method == 'PUT':
            print 'in put'
            item = _getsub(customerid,podid)
            if item:
                if _putsub(customer, podid):
                    return app.make_response('subscription updated')
                else:
                    return 'error happened', 400
            else:
                return 'object not found', 404
    except Exception:
        return 'bad request', 400

def _getsub(customerid, podid):
    try:
        print 'in _getsub'
        query = "select subid, customerid, podid from subs where customerid = '%s' and podid = '%s'" % (customerid, podid)
        curA.execute(query)
        print 'query sub',query
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None

def _getsub_by_customerid(customerid):
    try:
        print 'in _getsub'
        query = "select subid, customerid, podid from subs where customerid = '%s'" % customerid
        curA.execute(query)
        print 'query sub',query
        item = curA.fetchone()
        if item is not None:
            return item
        else:
            return None
    except Exception:
        return None

def _addsub(customerid, podid):
    try:
        print 'in _addsub'
        customer = _getcustomer_byid(customerid)
        podcast = _getpodcast_byid(podid)
        if customer and podcast:
            query = "insert into subs (customerid, podid) values ('%s', '%s')" % (customerid, podid)
            print query
            curA.execute(query)
            cnx.commit()
            return True
        else:
            return False
    except Exception:
        return False

def _deletesub(customerid):
    try:
        print 'in _delsub'
        query = "delete from subs where customerid = '%s'" % customerid
        print query
        curA.execute(query)
        cnx.commit()
        return True
    except Exception:
        return False

def _putsub(customerid,podid):
    try:
        print 'in _putsub'
        query = "update subs set podid='%s' where customerid=('%s')" %(podid,customerid)
        print query
        curA.execute(query)
        item =curA.fetchone()
        print item
        cnx.commit()
        return True
    except Exception:
        return False


@app.route('/download', methods=['POST'])
def DownloadSub():
    try:
        customername = request.args.get('customername')
        downloader_url = request.args.get('downloader_url')
        """get the sub of the user by name
        send the sub to downloader which should start the download"""
        item = _getcustomer(customername)
        if item:
            (customerid, name) = item
            sub = _getsub_by_customerid(customerid)
            if sub:
                (subid,customerid,podid) = sub
                pod= _getpodcast_byid(podid)
                if pod:
                    (podid, podname, url) = pod
                    print url
                    data=_parseurl(url)
                    """post the json data to the downloader url"""
                    print 'finished parse url'
                    _post(downloader_url,data)
                    return app.make_response('url posted')
                else:
                    return 'podcast not found'
            else:
                return 'customer not have any subscriptions'
        else:
            """customer not found"""
            return 'customer not found', 404


    except Exception as e:
        print e.message
        return 'bad request', 400


def _parseurl(rss_url):
    res = req.get(rss_url)
    print res
    print res.content
    pods = Podcast.Podcast(res.content)
    '''only send one item now'''
    item = pods.items[0]
    data=item.enclosure_url.split("?apikey=")[0]
    print data
    return data

def _post(url_to_post, data):
    c = pycurl.Curl()
    to = url_to_post +'?url='+str(data)
    print to
    c.setopt(c.URL, to)
    c.perform()
    c.close()

@app.errorhandler(404)
def page_not_found(error):
    return 'object not found', 404

if __name__ == '__main__':
    app.run()