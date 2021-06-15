echo "select distinct(email) from OL_CONTACT where tenant_id = 'cbc' and email is not null and stage in ('Midweek') ;" | mysql kp_db | paste -sd, | sed  -e 's/email,//' > mws.txt

