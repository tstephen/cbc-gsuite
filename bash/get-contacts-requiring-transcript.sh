echo "select concat(first_name, ' ', last_name), concat(address1, ',', post_code) from OL_CONTACT c JOIN OL_CONTACT_CUSTOM cc on c.id = cc.contact_id where tenant_id = 'cbc' and cc.name='transcripts'  and stage in ('9:15','11:15','COTG','Midweek') order by last_name;" | mysql kp_db > cbc-address.txt

