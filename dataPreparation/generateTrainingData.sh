#!/bin/bash
#Download and unzip training dataset
wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz && gunzip kddcup.data.gz
#Filter only selected columns
awk -F ',' '{print $1","$3","$5","$6","$23","$24","$32","$33","$35","$36","$38","$42}' kddcup.data > kddcup_mod.data
awk '!seen[$0]++' kddcup_mod.data > kddcup_mod_1.data
#Remove fullstop from the end of each line
sed -i 's/.$//' kddcup_mod_1.data
#Enumerate the names of services and attacks
python normalize.py
#Final normalized file is kddcup_mod_2.data
awk -F ',' '$12=='0'{print $0}' kddcup_mod_2.data > normal.data
awk -F ',' '$12=='1'{print $0}' kddcup_mod_2.data > dos.data
awk -F ',' '$12=='2'{print $0}' kddcup_mod_2.data > probe.data
awk -F ',' '$12=='3'{print $0}' kddcup_mod_2.data > u2r.data
awk -F ',' '$12=='4'{print $0}' kddcup_mod_2.data > r2l.data
shuf -n 2500 normal.data >> update_train.data
shuf -n 3500 dos.data >> update_train.data 
shuf -n 3550 probe.data >> update_train.data 
#cat r2l.data >> update_train.data 
cat u2r.data >> update_train.data 
shuf update_train.data > train.data
rm normal.data dos.data probe.data u2r.data r2l.data kddcup_mod* update_train.data
sed -i 's/,/ /g' train.data
sed -i '1s/^/2.0 0.00005\n/' train.data
sed -i '1s/^/9602 4 12\n/' train.data
echo "Copying train.data file under ../AFCM"
cp train.data ../AFCM/
echo "Done generating training file ../AFCM/train.data."
