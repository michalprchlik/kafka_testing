run-kafka:
	podman run \
	-d \
	--name kafka \
	-p 9092:9092 \
	-p 9094:9094  \
	--network host    \
	-e ALLOW_PLAINTEXT_LISTENER=yes   \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=127.0.0.1:2181  \
    -e KAFKA_LISTENERS=INTERNAL://0.0.0.0:9092,OUTSIDE://0.0.0.0:9094 \
    -e KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka:9092,OUTSIDE://localhost:9094 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,OUTSIDE:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL \
    -e KAFKA_CLIENT_USERS=user,user1 \
    -e KAFKA_CLIENT_PASSWORDS=kyndryl,kyndryl1 \
    bitnami/kafka:latest

run-zookeeper:
    podman run \
    -d \
    --name zookeeper     \
    --network host     \
    -e ALLOW_ANONYMOUS_LOGIN=yes     \
    bitnami/zookeeper:latest

