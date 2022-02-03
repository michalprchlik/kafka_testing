from kafka import KafkaConsumer, TopicPartition
import logging
import json
from time import sleep


logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s %(levelname)s %(message)s',
	datefmt='%H:%M:%S'
)
size = 1000000

def run_loader(url):
	logging.info(f"AIC loader started processing of file on url={url}")
	sleep(1)

consumer1 = KafkaConsumer(bootstrap_servers='localhost:9094',
auto_offset_reset = 'earliest', group_id = 'test', enable_auto_commit=False)
def kafka_python_consumer1():
    consumer1.subscribe(['topic1'])
    for msg in consumer1:
      logging.info(msg.value.decode('UTF-8'))
      logging.info(f"msg.topic={msg.topic}, msg.partition={msg.partition}, msg.offset={msg.offset}, msg.key={msg.key}, msg.value={msg.value}")
      data = json.loads(msg.value.decode('UTF-8'))
      if "sfs_scan_file" in data:
         run_loader(data['sfs_scan_file'])
      consumer1.commit()

consumer2 = KafkaConsumer(bootstrap_servers='localhost:9094')
def kafka_python_consumer2():
    consumer2.assign([TopicPartition('topic1', 1)])
    for msg in consumer2:
        print(msg)

consumer3 = KafkaConsumer(bootstrap_servers='localhost:9094')
def kafka_python_consumer3():
    partition = TopicPartition('topic1', 0)
    consumer3.assign([partition])
    last_offset = consumer3.end_offsets([partition])[partition]
    for msg in consumer3:
        if msg.offset == last_offset - 1:
            break

kafka_python_consumer1()