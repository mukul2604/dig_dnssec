#! /bin/bash
set -x
file=$1
rm -f $file 
echo Dumping output to $file
for i in {1..10}
do
  python mydig.py google.com   A False  
done

for i in {1..10}
do
  python mydig.py youtube.com   A False  
done

for i in {1..10}
do
  python mydig.py facebook.com   A False  
done

for i in {1..10}
do
  python mydig.py baidu.com   A False  
done

for i in {1..10}
do
  python mydig.py yahoo.com   A False  
done

for i in {1..10}
do
  python mydig.py wikipedia.org   A False  
done

for i in {1..10}
do
  python mydig.py google.co.in   A False  
done

for i in {1..10}
do
  python mydig.py tmall.com   A False  
done

for i in {1..10}
do
  python mydig.py qq.com   A False  
done

for i in {1..10}
do
  python mydig.py amazon.com   A False  
done

for i in {1..10}
do
  python mydig.py sohu.com   A False  
done

for i in {1..10}
do
  python mydig.py google.co.jp   A False  
done

for i in {1..10}
do
  python mydig.py taobao.com   A False  
done

for i in {1..10}
do
  python mydig.py live.com   A False  
done

for i in {1..10}
do
  python mydig.py vk.com   A False  
done

for i in {1..10}
do
  python mydig.py twitter.com   A False  
done

for i in {1..10}
do
  python mydig.py 360.cn   A False  
done

for i in {1..10}
do
  python mydig.py linkedin.com   A False  
done

for i in {1..10}
do
  python mydig.py instagram.com   A False  
done

for i in {1..10}
do
  python mydig.py yahoo.co.jp   A False  
done

for i in {1..10}
do
  python mydig.py sina.com.cn   A False  
done

for i in {1..10}
do
  python mydig.py jd.com   A False  
done

for i in {1..10}
do
  python mydig.py google.de   A False  
done

for i in {1..10}
do
  python mydig.py reddit.com   A False  
done

for i in {1..10}
do
  python mydig.py google.co.uk   A False  
done

sed -i '' 's/[[:alnum:]]*$//' ./$file
