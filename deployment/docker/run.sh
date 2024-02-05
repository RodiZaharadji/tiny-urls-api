#!/usr/bin/env bash
set -e

echo "${FASTAPI_APP_FACTORY}"

exec uvicorn --factory "${FASTAPI_APP_FACTORY}" --host 0.0.0.0 --port "${FASTAPI_APP_RUN_PORT}" --reload
