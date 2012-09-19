from pyquery import PyQuery as pq
from urllib2 import urlopen
from codecs import open
import os
import re

from config import *

class USNewsPageFactory(object):
    def _get_page_path(path,school_root,page_type):
        return os.path.join(school_root ,page_type)

    def get_page(self,school_name , page_type = "index.html" , ignore_cache = False , url = ""):
        school_root = os.path.join(CACHE_ROOT_PATH , school_name)
        index_path = self._get_page_path(school_root ,page_type )

        if not os.path.exists(school_root):
            os.system("mkdir -p %s" %school_root)

        if ignore_cache:#ignore cache
            if url == "":raise ValueError("url cannot be empty in `ignore cache` mode")

            resp = urlopen(url)#the response
            content = resp.read()#get the content

            #save it as local
            print "caching index page for %s" %school_name
            f = open(index_path,"w","utf8")
            f.write(content)
            f.close()

            return USNewsSchoolPage(content)
        else:#use the cache
            return USNewsSchoolPage(open(index_path,"r","utf8").read())


class USNewsSchoolPage(pq):
    def _convert_currency(self,string):
        return int(string.replace("$","").replace(",",""))

    def getTuitionFees(self):
        dls = self.find(".stat-group").eq(0).find("dd dl")
        if len(dls) == 1:
            return dict([("tuition&fees", 
                self._convert_currency(dls.eq(0).find("dt").eq(0).text()))])
        else:
            d_ = {}
            d_["tuition&fees"] = dict((pq(dl).find("dd").eq(0).text() , self._convert_currency(pq(dl).find("dt").eq(0).text()) ) 
                for dl in self.find(".stat-group").eq(0).find("dd dl"))
            return d_
    def getTotalRank(self):
        span = self(".rankings-score").find("span").eq(0)
        return {"total_rank":int(span.text().strip("#")),
                "score":float(re.findall(r"(\d{1,2})\sout of" , span.attr("title"))[0])}

if __name__ == "__main__":
    factory = USNewsPageFactory()
    for line in open("usnew-urls.txt","r","utf8").readlines():
        univ_name,usnews_url = line.split()
        #page = factory.get_page(univ_name,ignore_cache = True,url = usnews_url)
        page = factory.get_page(univ_name)
        print univ_name , page.getTuitionFees()

