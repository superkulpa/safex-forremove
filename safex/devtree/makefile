all: AK-GPIO-Test-00A0.dtbo

AK-GPIO-Test-00A0.dtbo: AK-GPIO-Test.dts
	dtc -O dtb -o AK-GPIO-Test-00A0.dtbo -b 0 -@ AK-GPIO-Test.dts

install: AK-GPIO-Test-00A0.dtbo
	cp ./AK-GPIO-Test-00A0.dtbo /lib/firmware
	./setdt

clean:
	rm -f AK-GPIO-Test-00A0.dtbo
#	echo -8 > $SLOTS
#	/lib/firmware/AK-GPIO-Test-00A0.dtbo
# AK-GPIO mustbe on 8 slot, check it before clean ( cat /sys/devices/bone_capemgr*/slots )	
	