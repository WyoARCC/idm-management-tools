#!/bin/bash

# Get all email addresses stored in IDM for enabled users in the mount moran group

# Get users in group
memberlist=$(ipa group-show mountmoran | grep "Member users:" | cut -d ':' -f 2 | sed "s/,/ /g")

# Iterate through the memberlist
for user in $memberlist; do
	
	# Pull user information
	userinfo=$(ipa user-find --login=$user --all)

	# Check to see if user is disabled
	disabled=$(echo "$userinfo" | grep "Account disabled:" | cut -d ':' -f 2 | sed 's/ //g')

	if [ $disabled == 'False' ]; then
		email=$(echo "$userinfo" | grep "Email address:" | cut -d ':' -f 2)
		displayname=$(echo "$userinfo" | grep "Display name:" | cut -d ':' -f 2)

		echo "$user $displayname $email"
	fi

done

exit 0
