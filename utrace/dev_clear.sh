#!/system/bin/sh

PART_DIR=/sdcard/adafs/app-part

if [ $# -ne 2 ]; then
	echo "Usage: $0 AppAlias FilesystemName"
	exit 1
fi

echo 5 > /proc/sys/vm/dirty_background_ratio
echo 500 > /proc/sys/vm/dirty_writeback_centisecs

app=$1
fs_name=$2
part_file=$PART_DIR/$1.part

if [ ! -f $part_file ]; then
	echo "$0: Failed to open specified file: $part_file"
	exit 1
fi

args=(`cat $part_file`)
nr=$((${#args[@]}/2))

i=0; while test $i -lt $nr;
do
	dir=${args[i*2]%'/'}
	dev=${args[i*2+1]}
	for pid in `ps | grep $app | awk '{print $2}'`
	do
		kill -9 $pid
	done
	umount $dir
	if [ $? -ne 0 ]; then
		echo "$0: Failed to umount: $dir"
	fi
	rm -r $dir.bak
	i=$(($i+1))
done

if [ $fs_name = "eafs" ] || [ $fs_name = "bafs" ]; then
	rmmod $fs_name
fi

if [ $? = 0 ]; then
	echo "$0: Tracing settings cleared."
fi

