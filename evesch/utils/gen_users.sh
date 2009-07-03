#!/bin/sh

num=180
cat names.txt | while read name
do
  username=`echo "$name" | tr A-Z a-z`
  (( num = $num + 1 ))  
echo "user_email = UserEmail(email_label = '${username}', email_address='${username}@evesch.com',email_isDefault=True)"
echo "user_email.save()"
echo "user${num} = User(username='${username}',email_addresses=user_email)"
echo "user${num}.first_name = '${name}'"
echo "user${num}.last_name = 'Hot'"
echo "user${num}.is_superuser=False"
echo "user${num}.is_staff=False"
echo "user${num}.set_password('1234')"
echo "user${num}.save()"
echo "user${num}.user_organizations.add(org1)"
echo "print ' Created: ' + user${num}.username"
 
done
