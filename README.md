# kafka_testing

https://towardsdatascience.com/3-libraries-you-should-know-to-master-apache-kafka-in-python-c95fdf8700f2
https://kafka.apache.org/quickstart
https://rmoff.net/2018/08/02/kafka-listeners-explained/
https://kafka-python.readthedocs.io/en/master/usage.html

```
docker run -d --name zookeeper-server     --network host     -e ALLOW_ANONYMOUS_LOGIN=yes     bitnami/zookeeper:latest


docker run -d --name kafka-server   -p 9092:9092 -p 9094:9094  --network host     -e ALLOW_PLAINTEXT_LISTENER=yes    \
-e KAFKA_CFG_ZOOKEEPER_CONNECT=127.0.0.1:2181  \
-e KAFKA_LISTENERS=INTERNAL://0.0.0.0:9092,OUTSIDE://0.0.0.0:9094 \
-e KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka:9092,OUTSIDE://localhost:9094 \
-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,OUTSIDE:PLAINTEXT \
-e KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL \
   bitnami/kafka:latest
```

```
python3 -m pip install kafka-python --user
```

/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic sfs_scan_files --bootstrap-server localhost:9092


/opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic sfs_scan_files --from-beginning --bootstrap-server localhost:9092





















