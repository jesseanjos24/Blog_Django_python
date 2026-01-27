#!/bin/sh

set -e

weit_psql.sh

collectstatic.sh
migrate.sh

runserver.sh
