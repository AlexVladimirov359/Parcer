#!/usr/bin/env python3
from Parser import Parser
from MongoRepository import MongoRepository

Parser(MongoRepository("ati")).parse()