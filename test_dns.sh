#! /bin/bash
set -x
file=$1
rm -f $file
echo Dumping output to $file
for i in {1..10}
do
   (time dig google.com A) &> temp
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo google.com, $n >> $file 
done

for i in {1..10}
do
  (time dig youtube.com A) &> temp
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo youtube.com, $n >> $file
done

for i in {1..10}
do
  (time dig  facebook.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo facebook.com, $n >> $file
done

for i in {1..10}
do
  (time dig  baidu.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo baidu.com, $n >> $file
done

for i in {1..10}
do
  (time dig  yahoo.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo yahoo.com, $n >> $file
done

for i in {1..10}
do
  (time dig  wikipedia.org   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo wikipedia.org, $n >> $file
done

for i in {1..10}
do
  (time dig  google.co.in   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo google.co.in, $n >> $file
done

for i in {1..10}
do
  (time dig  tmall.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo tmall.com, $n >> $file
done

for i in {1..10}
do
  (time dig  qq.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo qq.com, $n >> $file
done

for i in {1..10}
do
  (time dig  amazon.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo amazon.com, $n >> $file
done

for i in {1..10}
do
  (time dig  sohu.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo sohu.com, $n >> $file
done

for i in {1..10}
do
  (time dig  google.co.jp   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo google.co.jp, $n >> $file
done

for i in {1..10}
do
  (time dig  taobao.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo taobao.com, $n >> $file
done

for i in {1..10}
do
  (time dig  live.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo live.com, $n >> $file
done

for i in {1..10}
do
  (time dig  vk.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo vk.com, $n >> $file
done

for i in {1..10}
do
  (time dig  twitter.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo twitter.com, $n >> $file
done

for i in {1..10}
do
  (time dig  360.cn   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo 360.cn, $n >> $file
done

for i in {1..10}
do
  (time dig  linkedin.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo linkedin.com, $n >> $file
done

for i in {1..10}
do
  (time dig  instagram.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo instagram.com, $n >> $file
done

for i in {1..10}
do
  (time dig  yahoo.co.jp   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo yahoo.co.jp, $n >> $file
done

for i in {1..10}
do
  (time dig  sina.com.cn   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo sina.com.cn, $n >> $file
done

for i in {1..10}
do
  (time dig  jd.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo jd.com, $n >> $file
done

for i in {1..10}
do
  (time dig  google.de   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo google.de, $n >> $file
done

for i in {1..10}
do
  (time dig  reddit.com   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo reddit.com, $n >> $file
done

for i in {1..10}
do
  (time dig  google.co.uk   A) &> temp  
   grep real temp &> temp1
   n=$(sed 's/.*m\(.*\)s/\1/' temp1)
   echo google.co.uk, $n >> $file
done

rm -f temp
rm -f temp1
