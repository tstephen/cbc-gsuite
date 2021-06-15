echo "select distinct(email) from OL_CONTACT where tenant_id = 'cbc' and email is not null and email != '' and stage in ('11:15','COTG','Midweek') ;" | mysql kp_db | paste -sd, | sed  -e 's/email,//' > except915.txt

