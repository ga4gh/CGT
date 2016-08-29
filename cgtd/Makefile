all: start

start:
	docker-compose up -d

stop:
	docker-compose down

clean: stop

reset:
	# Reset steward to no submissions and no peers and then gc
	docker-compose exec -T ipfs sh -c "echo '{\"domain\": \"cgt.lorem.edu\", \"submissions\": [], \"peers\": []}' | ipfs add -q | xargs ipfs name publish"

build:
	docker-compose build

test:
	docker-compose run cgtd py.test -p no:cacheprovider -s -x

push:
	docker tag cgtd:latest robcurrie/cgtd:latest
	docker images | grep cgtd
	docker push robcurrie/cgtd:latest

pull:
	git pull
	docker pull ipfs/go-ipfs:latest
	docker pull robcurrie/cgtd:latest

shell:
	docker-compose run cgtd /bin/sh

update_pip_packages:
	docker-compose run cgtd "pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U"

update_requirements:
	docker-compose run cgtd pip freeze > requirements.txt
