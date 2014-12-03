#!/bin/python

import json
from boto import connect_iam
from urllib import unquote

iam = connect_iam()

def get_users():
	data = iam.get_all_users()
	users = data['list_users_response']['list_users_result']['users']

	return users

def get_policies_rules(user):
	policy_documents = []

	data = iam.get_groups_for_user(user)
	data = data.values()[0]
	data = data['list_groups_for_user_result']['groups']

	# I don't actually have an example of how it whould look like
	# so let's leave it like this for the moment
	
	# policies = iam.get_all_user_policies()['list_user_policies_response']['list_user_policies_result']['policy_names']
	policies = {}

	groups = [group['group_name'] for group in data]

	for group in groups:
		data = iam.get_all_group_policies(group)
		policies[group] = data['list_group_policies_response']['list_group_policies_result']['policy_names']

	for group in policies.keys():
		for policy in policies[group]:
			data = iam.get_group_policy(group, policy)
			data = data['get_group_policy_response']['get_group_policy_result']['policy_document']
			policy_documents.append(json.loads(unquote(data)))

	return policy_documents
