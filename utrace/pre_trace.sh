#!/system/bin/sh

if [ $# -ne 2 ]; then
	echo "Usage: $0 DirDevListFile RFFSKernelModule"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "Failed to open specified file: $1"
	exit 1
fi

if [ ! -f $2 ]; then
	echo "Failed to locate kernel module file: $2"
	exit 1
fi

args=(`cat $1`)
nr=$((${#args[@]}/2))

insmod $2
echo 3600000 > /proc/sys/vm/dirty_writeback_centisecs

i=0; while test $i -lt $nr;
do
	dir=${args[i*2]}
	dev=${args[i*2+1]}
	fuser -k $dir
	mkdir -p $dir.bak
	rm -r $dir.bak/* 2>/dev/null
	cp -r $dir/* $dir.bak/
	mount -t rffs $dev $dir
	if [ $? -ne 0 ]; then
		echo "Failed to mount $dev on $dir"
		exit 2
	else
		rm -r $dir/* 2>/dev/null
		cp -r $dir.bak/* $dir/
		chmod -R 777 $dir
		echo "$dir prepared for tracing."
	fi
	i=$(($i+1))
done

for log in `ls /sys/fs/rffs/ | grep log*`
do
	echo 1000000000 > /sys/fs/rffs/$log/staleness_limit
        echo $log" staleness_limit="`cat /sys/fs/rffs/$log/staleness_limit`
	echo 0 > /sys/fs/rffs/$log/staleness_sum
        echo $log" staleness_sum="`cat /sys/fs/rffs/$log/staleness_sum`
done

