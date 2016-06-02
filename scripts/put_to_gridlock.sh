arr[0]="up"
arr[1]="warn"
arr[2]="down"

while true
do
  for service in nova-api cinder-api glance-api neutron-api swift-api horizon heat-api keystone-api mysql mongodb memcached haproxy
  do
    for loc in london "new-york" sydney tokyo berlin vancouver
    do
      rand=$[ $RANDOM % 3 ]
      DATE=`date +%s`
      curl -q -i -H "Content-Type: application/json" -X PUT -d '{"description":"'${service}'", "service":"'${service}'","status":"'${rand}'","location":"'${loc}'","env":"prd","timestamp":"'${DATE}'"}' http://localhost:5000/gridlock/api/v0.1/
    done
  done
sleep 60
done
