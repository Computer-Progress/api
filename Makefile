include .env

.PHONY: up-test

test:
	(sudo docker-compose -f test.docker-compose.yml up -d && \
	sudo docker-compose -f test.docker-compose.yml exec backend-tests pytest);\
	sudo docker-compose -f test.docker-compose.yml down
