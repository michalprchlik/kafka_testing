import time
from kafka import KafkaProducer
import logging
from time import sleep
from json import dumps
from kafka.errors import KafkaError


logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s %(levelname)s %(message)s',
	datefmt='%H:%M:%S'
)

msg = ('kafkakafkakafka' * 20).encode()[:100]
size = 1000000

logging.info("Start")
# logging.error(kafka.__version__)
#producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(bootstrap_servers='localhost:9094', security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN', 
						sasl_plain_username='user', sasl_plain_password='bitnami', api_version=(0,11,5),
              value_serializer=lambda x: dumps(x).encode('utf-8'))
# Asynchronous by default
future = producer.send('topic1', b'raw_bytes')

# Block for 'synchronous' sends
try:
	record_metadata = future.get(timeout=5)
	logging.info(record_metadata)
except KafkaError as exc:
	# Decide what to do if produce request failed...
	logging.error(exc)
	pass

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
						 value_serializer=lambda x: 
						 dumps(x).encode('utf-8'))
for e in range(1000):
	logging.info("+++++++++++kafka_python_producer_sync")
	data = {'number' : e}
	producer.send('topic1', value=data)
	sleep(1)



producer = KafkaProducer(bootstrap_servers='localhost:9092')
logging.info("End")

def kafka_python_producer_sync(producer, size):
	logging.info("+++++++++++kafka_python_producer_sync")
	for _ in range(size):
		logging.info("kafka_python_producer_sync")
		future = producer.send('topic1', msg)
		result = future.get(timeout=60)
	producer.flush()
	
def success(metadata):
	print(metadata.topic)

def error(exception):
	print(exception)

def kafka_python_producer_async(producer, size):
	for _ in range(size):
		producer.send('topic', msg).add_callback(success).add_errback(error)
	producer.flush()