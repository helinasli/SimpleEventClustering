from sklearn.metrics.pairwise import cosine_similarity
import random
import string
import json
import numpy as np
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import KMeans
from pymongo import MongoClient


def generate_random_event():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['eventdb']
    collection = db['events']
    events = []
    for i in range(10):
        event = {}
        event["producer"] = "Server" + str(random.randint(1, 2))
        event["timestamp"] = str(datetime.datetime.now())
        event["type"] = random.choice(["alert", "clear"])
        event["message"] = random.choice(["apple", "home", "book"]) + ' ' + random.choice(
            ["apple", "home", "book"]) + ' ' + random.choice(["apple", "home", "book"])
        event["kpi"] = random.choice(
            ["cpu_usage", "memory_usage", "disk_usage"])
        event["kpi_profile"] = random.choice(["critical", "warning", "normal"])
        event["serenity"] = random.choice(["high", "medium", "low"])
        event["informer"] = random.choice(
            ["informer1", "informer2", "informer3"])
        event["unwanted_key1"] = random.choice(
            ["unwanted_value1", "unwanted_value2", "unwanted_value3", "unwanted_value4"])
        events.append(event)
    with open('events.json', 'w') as outfile:
        json.dump(events, outfile)
    collection.insert_many(events)
    return events


def filter_events(events):
    required_keys = ["producer", "timestamp",
                     "type", "message", "kpi", "kpi_profile"]
    for event in events:
        for key in list(event.keys()):
            if key not in required_keys:
                del event[key]
    return events


def filter_stored_events():
    with open('events.json', 'r') as infile:
        events = json.load(infile)
        filtered_events = filter_events(events)
    with open('filtered_events.json', 'w') as outfile:
        json.dump(filtered_events, outfile)
    return filtered_events


def similarity_score(event1, event2):
    text1 = event1['producer']*5 + ' ' + event1['timestamp'] + ' ' + event1['type'] + ' ' + event1['message'] + \
        ' ' + event1['kpi'] + ' ' + event1['kpi_profile'] + \
        ' ' + event1['serenity'] + ' ' + event1['informer']
    text2 = event2['producer'] + ' ' + event2['timestamp'] + ' ' + event2['type'] + ' ' + event2['message'] + \
        ' ' + event2['kpi'] + ' ' + event2['kpi_profile'] + \
        ' ' + event2['serenity'] + ' ' + event2['informer']
    texts = [text1, text2]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(X[0], X[1])

    return similarity[0][0]


def createCollection(name):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['clusterdb']
    collection = db[name]
    return collection


def event_compare(event_new, event_cluster):
    print(similarity_score(event_new, event_cluster))
    return similarity_score(event_new, event_cluster) > 0.5


def clear_database():
    client = MongoClient("mongodb://localhost:27017/")
    client.drop_database('clusterdb')


def average_event(collection_name):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['clusterdb']
    collection = db[collection_name]
    events = list(collection.find({}))
    average_event = {}
    for i in range(len(events)):
        for key in events[i].keys():
            values = [event[key] for event in events]
            most_frequent_value = max(set(values), key=values.count)
            average_event[key] = most_frequent_value
    print(collection_name, " average event:")
    print(average_event)
    print("")
    return average_event


def clustering(event):
    print("")
    print("")
    print("YENİ EVENT EKLENİYOR")
    client = MongoClient("mongodb://localhost:27017/")
    db = client['clusterdb']

    if (len(db.list_collection_names()) == 0):
        db.create_collection("cluster0")
        print("ilk cluster oluşturuldu")
        db["cluster0"].insert_one(event)
        print("event cluster 0' a eklendi")
    else:
        print("Var olan clusterlar: ", db.list_collection_names())
        is_event_added = False
        for i in db.list_collection_names():
            if (event_compare(event, average_event(i))):
                db[i].insert_one(event)
                print("event " + i + "'a eklendi")
                is_event_added = True
        if (is_event_added == False):
            db.create_collection(
                "cluster" + str(len(db.list_collection_names())))
            db["cluster" +
                str(len(db.list_collection_names()) - 1)].insert_one(event)
            print("event: " + "cluster" +
                  str(len(db.list_collection_names())-1) + " eklendi")
            print("Yeni clusterlar:", db.list_collection_names())
            return


with open('events.json', 'r') as infile:
    events = json.load(infile)

clear_database()
for (i, event) in enumerate(events):
    clustering(event)
