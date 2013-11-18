#!/system/bin/sh

PART_DIR=/sdcard/adafs/app-part
KO_DIR=/sdcard/adafs/

if [ $# -ne 2 ]; then
	echo "Usage: $0 AppAlias FilesystemName[eafs|bafs|ext4|ramfs]"
	exit 1
fi

app=$1
fs_name=$2

part_file=$PART_DIR/$app.part
if [ ! -f $part_file ]; then
	echo "$0: App's dir-dev file (.part) does not exit: $part_file"
	exit 1
fi

if [ $fs_name = "eafs" ] || [ $fs_name = "bafs" ]; then
	if [ ! -f $KO_DIR/$fs_name.ko ]; then
		echo "$0: Failed to locate kernel module file: $KO_DIR/$fs_name.ko"
		exit 1
	fi
	fs_type="adafs"
	insmod $KO_DIR/$fs_name.ko
else
	fs_type=$fs_name
fi

args=(`cat $part_file`)
nr=$((${#args[@]}/2))

if [ $fs_type = "adafs" ]; then
	echo 90 > /proc/sys/vm/dirty_background_ratio
	echo 3600000 > /proc/sys/vm/dirty_writeback_centisecs
	echo 'Adjusted dirty page parameters.'
fi

i=0; while test $i -lt $nr;
do
	dir=${args[i*2]%/}
	dev=${args[i*2+1]}

	par_dir=${dir%/*}
	end_dir=${dir##*/}
	user=`ls -l $par_dir | grep ' '$end_dir$ | awk '{print $2}'`
	group=`ls -l $par_dir | grep ' '$end_dir$ | awk '{print $3}'`

	for pid in `ps | grep $app | awk '{print $2}'`
        do
                kill -9 $pid
        done
	mkdir -p $dir.bak
	rm -r $dir.bak/{,.[!.]}* 2>/dev/null
	cp -r $dir/. $dir.bak/
	mount -t $fs_type $dev $dir
	if [ $? -ne 0 ]; then
		echo "$0: Failed to mount $dev on $dir"
		exit 3
	else
		rm -r $dir/{,.[!.]}* 2>/dev/null
		cp -r $dir.bak/. $dir/
		find $dir | xargs chown $user:$group
		echo "$0: $dir prepared for tracing."
	fi
	i=$(($i+1))
done

if [ -d "/sys/fs/adafs" ]; then
	for log in `ls /sys/fs/adafs/ | grep log*`
	do
		echo 32768 > /sys/fs/adafs/$log/stal_limit_blocks
        	echo "$0: $log stal_limit_blocks="`cat /sys/fs/adafs/$log/stal_limit_blocks`
		echo 0 > /sys/fs/adafs/$log/staleness_sum
        	echo "$0: $log staleness_sum="`cat /sys/fs/adafs/$log/staleness_sum`
	done
	echo 1 > /sys/fs/adafs/trace/tracing_on
        echo "tracing_on="`cat /sys/fs/adafs/trace/tracing_on`
fi

#./ev_trace.o > /cache/adafs-ev-$app.`date +"%s"` &

