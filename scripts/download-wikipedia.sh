prefix=https://en.wikipedia.org/wiki
page=$1
output=$2
link=$prefix/$page
echo $link
wget $link --output-document=$output
