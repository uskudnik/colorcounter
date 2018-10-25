build:
		@docker-compose build

debug:
		@docker-compose run --entrypoint /bin/bash color-counter

test:
		@docker-compose run --entrypoint pytest color-counter