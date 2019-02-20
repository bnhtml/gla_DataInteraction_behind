#!/bin/bash
cd /root/datalink/sql_file
ssh root@1.255.1.202 "rm  -f /root/baas.oracle/db.search.sql"
#sleep 1
ssh root@1.255.1.202 "rm  -f /root/baas.mysql/db.search.sql"
#sleep 1
ssh root@1.255.1.202 "rm  -f /root/baas.esgnodb/db.search.sql"
#sleep 1
scp /root/datalink/sql_file/db.search.sql 1.255.1.202:/root/baas.oracle/db.search.sql
scp /root/datalink/sql_file/db.search.sql 1.255.1.202:/root/baas.mysql/db.search.sql
scp /root/datalink/sql_file/db.search.sql 1.255.1.202:/root/baas.esgnodb/db.search.sql
