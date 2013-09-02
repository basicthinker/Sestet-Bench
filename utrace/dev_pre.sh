#!/system/bin/sh

PART_DIR=/sdcard/adafs/app-part
KO_DIR=/sdcard/adafs/

if [ $# -ne 2 ]; then
	echo "Usage: $0 AppAlias FilesystemName"
	exit 1
fi

app=$1
fs_name=$2

part_file=$PART_DIR/$app.part
if [ ! -f $part_file ]; then
	echo "$0: App's dir-dev file (.part) does not exit: $part_file"
	exit 1
fi

if [ ! -f $KO_DIR/$fs_name.ko ]; then
	echo "$0: Failed to locate kernel module file: $KO_DIR/$fs_name.ko"
	exit 1
fi

args=(`cat $part_file`)
nr=$((${#args[@]}/2))

insmod $KO_DIR/$fs_name.ko
echo 3600000 > /proc/sys/vm/dirty_writeback_centisecs
if [ `cat /proc/sys/vm/dirty_writeback_centisecs` -ne '3600000' ]; then
	echo "$0: Failed to configure dirty_writeback_centisecs!"
	exit 2
fi

i=0; while test $i -lt $nr;
do
	dir=${args[i*2]%'/'}
	dev=${args[i*2+1]}
	for pid in `ps | grep $app | awk '{print $2}'`
        do
                kill -9 $pid
        done
	mkdir -p $dir.bak
	rm -r $dir.bak/{,.[!.]}* 2>/dev/null
	cp -r $dir/. $dir.bak/
	mount -t adafs $dev $dir
	if [ $? -ne 0 ]; then
		echo "$0: Failed to mount $dev on $dir"
		exit 3
	else
		rm -r $dir/{,.[!.]}* 2>/dev/null
		cp -r $dir.bak/. $dir/
		chmod -R 777 $dir
		echo "$0: $dir prepared for tracing."
	fi
	i=$(($i+1))
done

for log in `ls /sys/fs/adafs/ | grep log*`
do
	echo 1000000000 > /sys/fs/adafs/$log/staleness_limit
        echo "$0: $log staleness_limit="`cat /sys/fs/adafs/$log/staleness_limit`
	echo 0 > /sys/fs/adafs/$log/staleness_sum
        echo "$0: $log staleness_sum="`cat /sys/fs/adafs/$log/staleness_sum`
done

