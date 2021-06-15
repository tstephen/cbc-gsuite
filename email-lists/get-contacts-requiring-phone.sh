echo "select stage, concat(first_name, ' ', last_name) from OL_CONTACT where tenant_id = 'cbc' and (email is null or email = '') and (phone1 is not null and phone1 != '') and stage in ('9:15','11:15','COTG','Midweek') order by stage, last_name;" | mysql kp_db > cbc-phone.txt

