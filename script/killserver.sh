#!/usr/bin/env bash

ps aux|grep data_service.py|awk '{print $2}'|xargs kill
ps aux|grep core_service.py|awk '{print $2}'|xargs kill