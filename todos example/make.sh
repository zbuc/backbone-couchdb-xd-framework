#!/usr/bin/env bash

INDEX=index.html
BASEDIR=_site
DEBUG=$1

rm -rf $BASEDIR
mkdir -p $BASEDIR

jsflag=0
lessflag=0
echo "Gathering JS and LESS..."
while read line; do
    if [ "$line" == "[/JS]" ]; then
        jsflag=0
    elif [ $jsflag == 1 ]; then
        if [ "$line" != "" ]; then
            echo "    Including $line"
            if [ ! -v $DEBUG ]; then
                IFS='/' read -ra PARTS <<< "$line"
                str=""
                j=1
                for i in "${PARTS[@]}"; do
                    if [ $j -ne ${#PARTS[@]} ]; then
                        str="$str$i"
                    else
                        mkdir -p _site/$str
                        cat js/$line.js >> _site/$line.js
                    fi
                    j=$((j+1))
                done
                #cp --parents xx _site/$line.js
                #cat js/$line.js >> _site/$line.js
                echo "<script type='text/javascript' src='$line.js'></script>" >> _site/index.html
            else
                cat js/$line.js >> _site/js.big.js
            fi
        fi
    elif [ "$line" == "[JS]" ]; then
        jsflag=1
        if [ -v $DEBUG ]; then
            echo "<script type='text/javascript' src='js.js'></script>" >> _site/index.html
        fi
    elif [ "$line" == "[/LESS]" ]; then
        lessflag=0
    elif [ $lessflag == 1 ]; then
        echo "    Including $line"
        cat less/$line.less >> _site/less.less
    elif [ "$line" == "[LESS]" ]; then
        lessflag=1
        echo "<link href='css.css' rel='stylesheet' type='text/css'>" >> _site/index.html
    else
        echo "$line" >> _site/index.html
    fi
done < "$INDEX"

echo "Minifying JS..."
if [ -v $DEBUG ]; then
    uglifyjs _site/js.big.js > _site/js.js
    cat _site/js.big.js > _site/js.js
    rm _site/js.big.js
fi

echo "Copying images..."
cp -r img $BASEDIR/img

echo "Compiling LESS..."
lessc _site/less.less > _site/css.css
rm _site/less.less
