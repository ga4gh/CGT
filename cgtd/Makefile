all: start

start:
	docker-compose up -d

stop:
	docker-compose down

clean: stop

init:
	docker-compose run ipfs ipfs daemon --init

ipfs:
# Start ipfs daemon (assumes database is already initialized)
#	docker run -d --name ipfs \
#		-v `pwd`/data/export:/export \
#		-v `pwd`/data/ipfs:/data/ipfs \
#		-p 8080:8080 \
#		-p 4001:4001 \
#		-p 4002:4002/udp \
#		ipfs/go-ipfs:release

reset:
	# Reset steward to no submissions and no peers and then gc
	docker exec cgtd_ipfs_1 sh -c "echo '{\"domain\": \"cgt.lorem.edu\", \"submissions\": [], \"peers\": []}' | ipfs add -q | xargs ipfs name publish"
	echo $$?

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
