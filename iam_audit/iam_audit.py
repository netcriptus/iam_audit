#!/usr/bin/env python

import json
from boto import connect_iam
from urllib import unquote

iam = connect_iam()

def get_users():
	data = iam.get_all_users()
	users = data['list_users_response']['list_users_result']['users']

	return users

def get_rules_for_user(user):
    data = iam.get_groups_for_user(user)
    data = data.values()[0]
    data = data['list_groups_for_user_result']['groups']

    # I don't actually have an example of how it should look like
    # so let's leave it like this for the moment

    # user_policies = iam.get_all_user_policies()['list_user_policies_response']['list_user_policies_result']['policy_names']

    groups = [group['group_name'] for group in data]

    policy_documents = []
    for group in groups:
    	policy_documents += get_rules_for_group(group)

    return policy_documents

def get_rules_for_group(group):
    data = iam.get_all_group_policies(group)
    policies = data['list_group_policies_response']['list_group_policies_result']['policy_names']

    rules = []

    for policy in policies:
		data = iam.get_group_policy(group, policy)
		data = data['get_group_policy_response']['get_group_policy_result']['policy_document']
		rules.append(json.loads(unquote(data)))
    return rules

def get_all_policies():
    data = iam.get_all_groups()
    data = data['list_groups_response']['list_groups_result']['groups']
    
    groups = [group['group_name'] for group in data]
    
    policies = []
    for group in groups:
        policies += get_rules_for_group(group)
    
    return policies
    
data = get_all_policies()
for d in data:
    print d
    print

for item in list(data):
    data.remove(item)
    if item in data:
        print 'repeated item {}'.format(item)
    
