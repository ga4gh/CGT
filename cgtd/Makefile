all: start

start:
	docker-compose up -d

stop:
	docker-compose down

clean: stop

clean:
	sudo rm -rf data/*

init:
	# Create a new ipfs database including public/private key
	mkdir -p data/export
	mkdir -p data/ipfs
	sudo chmod -R 777 data
	docker run -it --rm --name ipfs \
		-v `pwd`/data/ipfs:/data/ipfs \
		--entrypoint=ipfs \
		ipfs/go-ipfs:release init
	# Default config file only listens on 127.0.0.1
	docker run -it --rm --name ipfs \
		-v `pwd`/data/ipfs:/data/ipfs \
		--entrypoint=ipfs \
		ipfs/go-ipfs:release config Addresses.API /ip4/0.0.0.0/tcp/5001
	docker run -it --rm --name ipfs \
		-v `pwd`/data/ipfs:/data/ipfs \
		--entrypoint=ipfs \
		ipfs/go-ipfs:release config Addresses.Gateway /ip4/0.0.0.0/tcp/8080

ipfs:
	# Start ipfs daemon (assumes database is already initialized)
	docker run -d --name ipfs \
		-v `pwd`/data/export:/export \
		-v `pwd`/data/ipfs:/data/ipfs \
		-p 8080:8080 \
		-p 4001:4001 \
		-p 4002:4002/udp \
		ipfs/go-ipfs:release

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
