#!/bin/bash
# set -e

# 执行 scrapy 命令得出来的打印结果赋值给变量: 变量名称=$(cmd命令)
scrapynames=$(scrapy list)
echo "the scrapy name is : $scrapynames"

# 查找该name，批量kill pid
for i in $scrapynames ; do
    echo "killing $i"
    ps -ef | grep "scrapy crawl $i" | grep -v grep | awk '{print $2}' | xargs kill -9 
done
ps -ef|grep chrome|grep -v grep|awk  '{print "kill -9 " $2}' |sh
