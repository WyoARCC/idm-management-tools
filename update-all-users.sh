#!/bin/bash

while read user; do
  echo Now attempting to update $user
  ./update-idm-user.py $user --uid
done < full_user_list
	
