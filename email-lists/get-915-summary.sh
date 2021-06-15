echo "select concat(first_name, ' ', last_name), phone1, concat(address1,',',town) from OL_CONTACT where tenant_id = 'cbc' and stage in ('9:15') order by last_name;" | mysql kp_db > 915-summary.txt

