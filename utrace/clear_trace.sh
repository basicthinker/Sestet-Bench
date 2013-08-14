#!/system/bin/sh

if [ $# -ne 2 ]; then
	echo "Usage: $0 DirDevListFile RFFSModuleName"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "Failed to open specified file: $1"
	exit 1
fi

args=(`cat $1`)
nr=$((${#args[@]}/2))

i=0; while test $i -lt $nr;
do
	dir=${args[i*2]}
	dev=${args[i*2+1]}
	fuser -k $dir
	umount $dir
	if [ $? -ne 0 ]; then
		echo "Failed to umount: $dir"
	fi
	rm -r $dir.bak
	i=$(($i+1))
done

rmmod $2
if [ $? = 0 ]; then
	echo 'Tracing settings cleared.'
fi

