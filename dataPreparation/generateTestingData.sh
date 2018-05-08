#!/bin/bash
wget http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz && gunzip corrected.gz
mv corrected corrected.data
#Filter only selected columns
awk -F ',' '{print $1","$3","$5","$6","$23","$24","$32","$33","$35","$36","$38","$42}' corrected.data > corrected_mod.data
awk '!seen[$0]++' corrected_mod.data > corrected_mod_1.data
#Remove fullstop from the end of each line
sed -i 's/.$//' corrected_mod_1.data
#Enumerate the names of services and attacks
python normalize_test.py
sed -i 's/,/ /g' corrected_mod_2.data
#Final normalized file is corrected_mod_2.data
awk '$12=='0'{print "xxxx yyyy "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11}' corrected_mod_2.data > normal_test.data
awk '$12=='1'{print "xxxx yyyy "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11}' corrected_mod_2.data > dos_test.data
awk '$12=='2'{print "xxxx yyyy "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11}' corrected_mod_2.data > probe_test.data
awk '$12=='3'{print "xxxx yyyy "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" "$10" "$11}' corrected_mod_2.data > u2r_test.data
rm corrected_mod*
