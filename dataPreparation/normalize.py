readf = open('kddcup_mod_1.data', 'r')
writef = open('kddcup_mod_2.data', 'w')
services = open('services.txt', 'r')
attacks = open('attacks.txt', 'r')
service_map = {}
attack_map = {}
count = 0

for service in services:
	service_map[service[:-1]] = str(count)
	count = count + 1
services.close()
for attack in attacks:
    attack_map[attack.split()[0]] = attack.split()[1]
attacks.close()

for line in readf:
    data=line.split(',')
    data[1] = service_map[data[1]]
    data[11] = attack_map[data[11][:-1]]
    str = ",".join(data )
    writef.write(str) 
    writef.write('\n')
readf.close()
writef.close()
