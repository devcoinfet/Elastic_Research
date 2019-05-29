"""
Simple example of querying Elasticsearch creating REST requests
"""
import requests
import json
import sys
from termcolor import colored

''''''
def search(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "match": {
                "content": term
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results




def format_results(results):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))



#here down written by me
def get_elastic_info(uri_in):
    print("\n")
    print(uri_in+" --> Target")
    try:
       response = requests.get(uri_in, timeout=3, verify=False)
       results = response.text
       return results
    except:
        pass


def get_data(host, indice):
    host_enum = "http://" + host + ":9200/" + indice + "/_search?size=1000&from=0"
    response = requests.get(host_enum, timeout=5, verify=False)
    results = response.text
    return results

#todo later just wrote this tonight real fast allot to finish and or fix
def get_cats(uri_in):
    uri_cats = uri_in + '/_cat/'
    skip_text = "=^.^="



def get_indices(uri_in):
    url_new = uri_in + "_cat/indices"
    response = requests.get(url_new, timeout=3, verify=False)
    results = response.text
    return results

def render_indices(text):
    text = text.splitlines()

    return text


if __name__ == '__main__':
    flagged_words = ['user','password','pass','uname','hash','passStore','admin']
    host = sys.argv[1]
    try:
       uri_search = 'http://' + host + ':9200/'
       elastic_info = get_elastic_info(uri_search)
       remote_indices = get_indices(uri_search)
       elastic_info_dict = json.loads(elastic_info)
       if elastic_info_dict:
          print('-' * 42)
          print(colored("Remote Elastic Search Endpoint Information ",'green'))
          print('-'*42)
          print(colored("Name:" + elastic_info_dict['name'], 'red'))
          print(colored("Cluster Name:"+elastic_info_dict['cluster_name'], 'red'))
          print(colored("Cluster uuid:" + elastic_info_dict['cluster_uuid'], 'yellow'))
          print(colored("version:" + elastic_info_dict['version']['number'], 'yellow'))
          print(colored("build_flavor:" + elastic_info_dict['version']['build_flavor'], 'yellow'))
          print(colored("build_date:" + elastic_info_dict['version']['build_date'], 'yellow'))
          print(colored("Lucene version:" + elastic_info_dict['version']['lucene_version'], 'yellow'))
          print(colored("tagline:" + elastic_info_dict['tagline'], 'red'))
          print('-' * 42)
          print(colored("Remote Elastic Search Indice Information ", 'green'))
          print('-' * 42)
          results2 = render_indices(remote_indices)

          for results in results2:
              cleaned = results.split()
              print(cleaned[2])

          print('-' * 54)

          print(colored("Remote Elastic Search Endpoint Indice Dump Information ",'green'))
          print('-' * 54)
          for results in results2:
              cleaned = results.split()
              print(cleaned[2])
              try:
                  if "user" in cleaned[2]:
                      data_dumped = get_data(host, cleaned[2])
                      print("Data Dumped For"+cleaned[2])
                      print(len(data_dumped))
                      print(data_dumped)
                      for words in flagged_words:
                          flagged = data_dumped.find(words)
                          if flagged:
                              print(colored(words+":Possible Credentials Detected ", 'red'))



              except:
                  pass

       else:
           pass

    except:
        pass

    
    '''
    results = search(uri_search, "fox")
    format_results(results)
    '''
