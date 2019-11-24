#!/bin/bash

find . -name '*.py' | entr pipenv run test

