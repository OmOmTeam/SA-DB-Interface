#!/usr/bin/env bash

export FLASK_APP=db_interface
export FLASK_ENV=development
flask "$@"
