#!/bin/sh

#args are template,ami, key, security gruop, and instance type,outputname
cat $1 | sed "s/IMAGE_VAL/$2/" | sed "s/KEY_VAL/$3/" | sed "s/SG_VAL/$4/" | sed "s/INSTANCE_TYPE/$5/" > $6
