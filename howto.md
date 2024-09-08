## kafka_test
$ docker network create kafka_network
b6b2803c150146d8a8bf67d3fce10ad1fc094fae6557048303d8eb8602d02719

$ docker compose up -d
$ docker compose ps
$ docker network inspect kafka_network

Connect to broker
$ docker exec -it broker /bin/bash
Create topic
$ root@broker:/# kafka-topics --bootstrap-server broker:9092 --create --topic sample-topic --partitions 3 replication-factor 1
Confirm
$ kafka-topics --bootstrap-server broker:9092 --describe --topic sample-topic

Connect to cli
$ docker exec -it cli /bin/bash
root@cli:/# kafka-console-consumer --bootstrap-server broker:29092 --topic sample-topic --group G1 --from-beginning
... waiting to receive message

Access from other terminal
$ docker exec -it cli /bin/bash
root@cli:/# kafka-console-producer --broker-list broker:29092 --topic sample-topic
> 
Send message

##
$ docker exec -it broker /bin/bash
root@broker:/# kafka-topics --bootstrap-server broker:9092 --create --topic topic-01 --partitions 3 replication-factor 1
root@broker:/# kafka-topics --bootstrap-server broker:9092 --describe --topic topic-01

$ docker compose up -d
$ docker compose ps

Connect cli
$ docker exec -it cli /bin/bash
root@cli:/# kafka-console-consumer --bootstrap-server broker:29092 --topic topic-01 --group G1 --from-beginning

Access from other terminal
$ docker exec -it kafka_tutorial-iot-1 /bin/bash
$ cd opt/
$ python IoTSampleData-v2.py --mode kf