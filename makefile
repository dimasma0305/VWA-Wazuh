run:
	docker compose down --volumes
	docker compose up --build

dev:
	docker compose -f docker-compose.dev.yml build --always-recreate-deps
	docker compose -f docker-compose.dev.yml up

stop:
	docker compose down --volumes
	docker compose -f docker-compose.dev.yml down --volumes 

gen-cert:
	docker-compose -f generate-indexer-certs.yml run --rm generator