run:
	docker compose -f docker-compose-ci.yaml up -d

stop:
	docker compose -f docker-compose-ci.yaml down && docker network prune --force