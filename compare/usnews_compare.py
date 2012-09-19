from school import USNewsPageFactory
from util import get_all_schools

from pprint import pprint

factory = USNewsPageFactory()
def _get_school_info(school_names):
    tuples = []
    for name in school_names:
        page = factory.get_page(name)
        info = page.getTuitionFees()
        info.update(page.getTotalRank())
        tuples.append( (name , info) )
    return tuples        

def get_fee(i):
    return i[1]["tuition&fees"]["out-of-state"] if isinstance(i[1]["tuition&fees"],dict) else i[1]["tuition&fees"]

def _sort_by_tuitions(school_names , n , desc = True):
    tfs = _get_school_info(school_names)
    sorted_schools = sorted(tfs,key = get_fee,reverse = desc )
    return sorted_schools[:n]

def get_top_n_cheapest(school_names , n):
    return _sort_by_tuitions(school_names , n , False)

def get_top_n_expensive(school_names , n):
    return _sort_by_tuitions(school_names , n , True)

def get_schools_with_tuition_below_n(school_names , n):
    tfs = _get_school_info(school_names)
    return sorted([tf for tf in tfs if get_fee(tf) < n] , key = get_fee , reverse = False)

if __name__ == "__main__":
    schools = get_all_schools()
    pprint(get_top_n_cheapest(schools,15))
    pprint(get_top_n_expensive(schools,15))
    #pprint(get_schools_with_tuition_below_n(schools,30000))
