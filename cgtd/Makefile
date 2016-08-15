all: start

start:
	docker-compose up

stop:
	docker-compose down

clean: stop

reset:
	# Reset steward to no submissions and no peers and then gc
	docker-compose exec ipfs sh -c "echo '{\"domain\": \"cgt.lorem.edu\", \"submissions\": [], \"peers\": []}' | ipfs add -q | xargs ipfs name publish"

build:
	docker-compose build

debug:
	docker stop cgtd || true && docker rm cgtd || true
	docker run --env FLASK_DEBUG=1 --name cgtd --rm -it \
		-v `pwd`:/app:ro \
		--network cgtd_default \
		--link cgtd_ipfs_1:ipfs \
		-p 3000:3000 \
		cgtd uwsgi --ini uwsgi.ini --python-autoreload=1 --processes=1 --threads=1

test:
	docker-compose exec cgtd py.test -p no:cacheprovider -s -x

push:
	docker tag cgtd:latest robcurrie/cgtd:latest
	docker images | grep cgtd
	docker push robcurrie/cgtd:latest

pull:
	git pull
	docker pull ipfs/go-ipfs:latest
	docker pull robcurrie/cgtd:latest

shell:
	docker-compose exec cgtd /bin/sh

update_pip_packages:
	docker-compose exec cgtd "pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U"

update_requirements:
	docker-compose exec cgtd pip freeze > requirements.txt
