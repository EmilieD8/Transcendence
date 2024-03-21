FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
	apt-get install -y curl && \
	apt-get install -y gnupg && \
	curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elastic.gpg && \
	echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list && \
	apt-get update && \
	apt-get -y install kibana && \
	mkdir -p /usr/share/kibana

COPY ./kibana.yml /etc/kibana/kibana.yml

ENV PATH="/usr/share/kibana/bin:${PATH}"

EXPOSE 5601

USER kibana

CMD ["kibana"]