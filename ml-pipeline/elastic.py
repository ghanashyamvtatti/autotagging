#!/usr/bin/env python
# coding: utf-8

import mlpipeline
from elasticsearch import Elasticsearch
from utils.kafkahelper import KafkaConnection

def run_kafka():
    conn = KafkaConnection()
    #download es and keep it running on the local sys while executing this
    es = Elasticsearch([{'host':'localhost', 'port':9200}])
    #data = "717_20170904123036/717_webhose-2017-01_20170904123520/blogs_0000001.json"

    #set up of index for es
    id = 0
    index = 'articles'
    doc_type = 'article'

    for data in conn.get_data():
        detail = mlpipeline.write_to_json(data)
        id += 1

        #handling url is empty or vocab is empty(in this case do not dump into es)
        if ((not detail['url']) or (not detail['vocab'])):
            continue

        #insert json into elasticsearch
        store = es.index(index=index, doc_type=doc_type, id=id, body=detail)
        print(store)

        #just to retrieve data from es
        retrieve = es.get(index=index, doc_type=doc_type, id=id)
        print(retrieve['_source'])

        #deleting the document(this statement can be deleted later)
        erase = es.delete(index=index, doc_type=doc_type, id=id)
        print(erase['result'])

if __name__ == "__main__":
    run_kafka()