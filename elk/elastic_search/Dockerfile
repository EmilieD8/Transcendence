FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
	apt-get install -y curl && \
	apt-get install -y gnupg && \
	apt-get install -y wget && \
	apt-get install -y apt-transport-https && \
	wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg && \
	echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list && \
	apt-get update && \
	apt-get install -y elasticsearch && \
	mkdir -p /usr/share/elasticsearch

ENV PATH="/usr/share/elasticsearch/bin:${PATH}"

EXPOSE 9200

USER elasticsearch

CMD ["elasticsearch"]
