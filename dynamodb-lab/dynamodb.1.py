from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import sys
from time import sleep

dynamodb = boto3.resource('dynamodb',  region_name='us-east-1', )


table = dynamodb.create_table(
   TableName='Movies',
   KeySchema=[
       {
           'AttributeName': 'year',
           'KeyType': 'HASH'  #Partition key
       },
       {
           'AttributeName': 'title',
           'KeyType': 'RANGE'  #Sort key
       }
   ],
   AttributeDefinitions=[
       {
           'AttributeName': 'year',
           'AttributeType': 'N'
       },
       {
           'AttributeName': 'title',
           'AttributeType': 'S'
       },

   ],
   ProvisionedThroughput={
       'ReadCapacityUnits': 5,
       'WriteCapacityUnits': 5
   }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='Movies')

table = dynamodb.Table('Movies')

i = 0
with open("data.json") as json_file:

    movies = json.load(json_file, parse_float = decimal.Decimal)
    for movie in movies:
        i = i + 1
        if i == 100:
            sys.exit()
        year = int(movie['year'])
        title = movie['title']
        actors = movie['actors']
        rating = movie['rating']
        running_time = movie['running_time_secs']

        print("Adding movie:", year, title, actors, rating, running_time)

        table.put_item(
           Item={
               'year': year,
               'title': title,
               'actors': actors,
               'rating': rating,
               'running_time': running_time
            }
        )
        sleep(.1)