#!/bin/sh
set -e

pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --clean --if-exists /backups/metabase_app.dump