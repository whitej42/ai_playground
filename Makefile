default: help

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9._-]+:.*#' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*# ";} {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

chainlit.build: # Build the Chainlit Docker image
	docker-compose -f chainlit/.docker/docker-compose.yaml build

chainlit.build-no-cache: # Build the Chainlit Docker image (no cache)
	docker-compose -f chainlit/.docker/docker-compose.yaml build --no-cache

chainlit.up: # Run the Chainlit Docker container
	docker-compose -f chainlit/.docker/docker-compose.yaml up -d

chainlit.up-build: # Build and run the Chainlit Docker container
	docker-compose -f chainlit/.docker/docker-compose.yaml up -d --build

chainlit.down: # Stop and remove the Chainlit Docker container
	docker-compose -f chainlit/.docker/docker-compose.yaml down

chainlit.restart: # Restart Chainlit container
	docker-compose -f chainlit/.docker/docker-compose.yaml down
	docker-compose -f chainlit/.docker/docker-compose.yaml up -d

chainlit.rebuild: # Force rebuild (no cache) and run
	docker-compose -f chainlit/.docker/docker-compose.yaml down
	docker-compose -f chainlit/.docker/docker-compose.yaml build --no-cache
	docker-compose -f chainlit/.docker/docker-compose.yaml up -d

chainlit.nuke: # Remove containers, images, volumes (DANGEROUS)
	docker-compose -f chainlit/.docker/docker-compose.yaml down --rmi local --volumes --remove-orphans

chainlit.logs: # View Chainlit container logs
	docker-compose -f chainlit/.docker/docker-compose.yaml logs -f

chainlit.exec: # Exec into Chainlit container
	 docker-compose -f chainlit/.docker/docker-compose.yaml exec -it chainlit bash