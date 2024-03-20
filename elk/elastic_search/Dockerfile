FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
	apt-get install -y curl && \
	apt-get install -y gnupg && \
	curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elastic.gpg && \
	echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list && \
	apt-get update && \
	apt-get install -y elasticsearch && \
	mkdir -p /usr/share/elasticsearch

COPY elasticsearch.yml /etc/elasticsearch/
COPY script_settings.sh /usr/share/elasticsearch
RUN chmod 777 /usr/share/elasticsearch/script_settings.sh

ENV PATH="/usr/share/elasticsearch/bin:${PATH}"

EXPOSE 9200

CMD ["/usr/share/elasticsearch/script_settings.sh"]
