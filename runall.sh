#!/bin/bash
set -e

if [ ! -d tmp ];then
  mkdir tmp
else
  echo dir exist
fi

# 执行 scrapy 命令得出来的打印结果赋值给变量: 变量名称=$(cmd命令)
scrapynames=$(scrapy list)
echo "the scrapy name is : $scrapynames"

# 循环启动 scrapy project name 进程，后台运行.
for i in $scrapynames; do
    echo "start $i"
    scrapy crawl $i &> tmp/${i}.log &
done