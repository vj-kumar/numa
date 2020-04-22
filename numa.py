#!/usr/bin/env python
# Author: Vijai Kumar K <vijaikumar.kanagarajan@gmail.com>
# Dt: 16 June 2018

# Dt: 04 November 2019
# Migrate to Todoist API v8. Remove priority.

import todoist
import json
import os
import sys
from argparse import ArgumentParser
from datetime import datetime

class Numa(object):
	def __init__(self, argv):
		token_file = os.path.join(os.getenv("HOME"), ".todoist")
		with open(token_file) as token:
			data = json.load(token)

		self.__api = todoist.TodoistAPI(data['token'])
		self.__projectList = {}
		try:
			self.__response = self.__api.sync()
		except:
			print("No network connection!!")
			sys.exit()
		self.__setupArgParser()
		self.__parserArgs(argv)

	def __setupArgParser(self):
		self.__parser = ArgumentParser()
		self.__parser.add_argument('-c', help="list all completed tasks", default=False, action='store_true')
		self.__parser.add_argument('-l', help="list with labels", default=False, action='store_true')

	def __parserArgs(self, argv):
		argv = self.__parser.parse_args()
		self.get_task_list(argv.c, argv.l)

	def get_project_by_id(self, project_id):
		return self.__api.projects.get_by_id(project_id)

	def get_user_by_id(self, user_id):
		collaborators = self.__api.state['collaborators']
		for collaborator in collaborators:
			if collaborator['id'] == user_id:
				return collaborator['full_name']
		return "Not Assigned"

        def get_label_by_id(self, label_id):
                return self.__api.labels.get_by_id(label_id)

	def get_task_list(self, completed, label=False):
		item_list = self.__api.state['items']
		sno = 1
                if label:
                    labelprint="Labels"
                else:
                    labelprint=""

                print "{:<3}: {:<15} {:<55} {:<15} {:<25}".format(
				"Sno",
				"Project",
				"Task",
				"Responsible",
                                labelprint)
		print "{:-<113}".format('-')
		for item in item_list:
			project = self.get_project_by_id(item['project_id'])
                        item_labels = []

                        if (project) and not (project['is_deleted']) and (item['checked'] == completed):
                                if label:
                                    for label in item['labels']:
                                        item_labels.append(self.get_label_by_id(label)['name'])
				project = self.get_project_by_id(item['project_id'])
				assigned_user = item['responsible_uid']
				assigned_user = self.get_user_by_id(assigned_user)
                                print "{:<3}: {:<15} {:<55} {:<15} {:<25}".format(
						sno,
						project['name'],
						item['content'],
						assigned_user,
                                                ', '.join(item_labels))
                                sno+=1
		print "{:-<113}".format('-')

def main(argv):
	numa = Numa(argv)

if __name__ == "__main__":
	main(sys.argv)
