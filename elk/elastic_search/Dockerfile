FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y curl && \
	apt-get install -y gnupg && \
	apt-get install -y zip && \
	apt-get install -y wget && \
	apt-get install -y apt-transport-https && \
	apt-get install ca-certificates && \
	wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg && \
	echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list && \
	apt-get update && \
	apt-get install -y elasticsearch && \
	mkdir -p /usr/share/elasticsearch && \
	chmod 777 /usr/share/elasticsearch

RUN echo "root:password" | chpasswd

ENV PATH="/usr/share/elasticsearch/bin:${PATH}"

COPY elasticsearch.yml /etc/elasticsearch/

COPY elasticsearch.yml /etc/elasticsearch/
COPY setup_script.sh .
COPY change_password.sh .

RUN chmod 777 setup_script.sh && chmod -R 777 /etc/elasticsearch/ && \
	chmod -R 777 /etc/elasticsearch/certs && chmod 777 change_password.sh

EXPOSE 9200

USER elasticsearch

CMD ["sh", "-c", "./setup_script.sh && /usr/share/elasticsearch/bin/elasticsearch -d && ./change_password.sh && sleep infinity"]
