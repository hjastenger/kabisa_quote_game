local_db_info:
	flyway -configFiles=flyway/conf/development.conf info

local_db_migrate:
	flyway -configFiles=flyway/conf/development.conf migrate

local_psql:
	psql -U admin -h localhost -p 5432 -d kabisa_db

local_db_reset:
	docker-compose up --no-deps --force-recreate -V --build postgres

rebuild_dev_db:
	make local_db_reset; sleep 4; make local_db_migrate
