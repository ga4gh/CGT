IPFS_VERSION := v0.4.3

ifdef DOMAIN
	domain=$$DOMAIN
else
	domain="lorem.edu"
endif

all: start

start:
	docker-compose up -d

stop:
	docker-compose down

clean: stop

clean:
	sudo rm -rf data/*

reset:
	echo "Resetting steard to no submissions, no peers, and domain = $(domain)"
	docker-compose exec ipfs sh -c "echo '{\"domain\": \"$(domain)\", \"submissions\": [], \"peers\": []}' | ipfs add -q | xargs ipfs name publish"

build:
	docker-compose build

debug:
	# Run cgtd out of the current directory with reloading after code change
	docker stop cgtd || true && docker rm cgtd || true
	docker run --name cgtd --rm -it \
		-v `pwd`:/app:ro \
		--link ipfs:ipfs \
		-p 5000:5000 \
		cgtd uwsgi --ini uwsgi.ini --python-autoreload=1 --processes=1 --threads=1

test:
	docker-compose run cgtd py.test -p no:cacheprovider -s -x

push:
	# Update docker hub (requires authentication)
	docker tag cgtd:latest robcurrie/cgtd:latest
	docker images | grep cgtd
	docker push robcurrie/cgtd:latest

pull:
	git pull
	docker pull ipfs/go-ipfs:$(IPFS_VERSION)
	docker pull robcurrie/cgtd:latest

populate:
	# Populate with data from the tests folder
	docker exec -it cgtd python tests/populate.py

submit:
	# Make a single test submission
	docker exec -it cgtd curl -X POST localhost:5000/v0/submissions \
        -F "a_field_name=a_field_value" \
        -F files[]=@tests/ALL/ALL-US__TARGET-10-PAKMVD-09A-01D.vcf

shell:
	docker-compose run cgtd /bin/sh
