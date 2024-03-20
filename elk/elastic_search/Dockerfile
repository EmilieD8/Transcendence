FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN echo "HELOOOOOO\n\n\n ELASTICSEARCH_USER: $ELASTICSEARCH_USER"

#since Elasticsearch requires Java to run, let’s install it first.
RUN apt-get update && \
	apt-get install -y curl && \
	apt-get install -y gnupg && \
	curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elastic.gpg && \
	echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list && \
	apt-get update && \
	apt-get install -y elasticsearch && \
	mkdir -p /usr/share/elasticsearch

COPY elasticsearch.yml /etc/elasticsearch/

ENV PATH="/usr/share/elasticsearch/bin:${PATH}"

RUN chown elasticsearch:elasticsearch -R /usr/share/elasticsearch && \
	mkdir -p /var/data/elasticsearch && \
	mkdir -p /var/log/elasticsearch && \
	chown -R elasticsearch:elasticsearch -R /var/data/elasticsearch && \
	chown -R elasticsearch:elasticsearch -R /var/log/elasticsearch
USER elasticsearch

EXPOSE 9200

CMD ["elasticsearch"]
