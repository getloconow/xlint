#!/bin/bash
if [ "$1" == "" ]
then
    exit
fi

target=$3
test=$2
cd $1
oldbranch=$target
git stash
git checkout $test
git merge --stat --no-commit --no-ff dev 2> /dev/null
files="$(git diff  --cached --name-only )"
IFS=$'\n'
echo "files : " $files


while read -r file; do
    echo $file
    IFS=$''
    file1=`git show $test:"$file" 2> /dev/null|cat`
    file2=`git show $oldbranch:"$file"|cat`
    echo $file2 > ../branch.file
    echo $file1 > ../test.file
    data=$(diff -u ../test.file  ../branch.file)
    ranges=$(python ../compile.py "$data") 
    mypy_out=$(python ../lint.py --python ~/py3/bin "$file" --mypy)
    pylint_out=$(python ../lint.py --python ~/py3/bin "$file" --pylint)
    python ../filter_output.py --data "$mypy_out" --ranges "$ranges" --mypy
    python ../filter_output.py --data "$pylint_out" --ranges "$ranges" --pylint
    rm -rf .mypy_cache
    IFS=$'\n'
done <<< "$(git diff --cached --name-only|cat)"



git merge --abort
if [ "$oldbranch" != "master" ]
then
    git checkout $oldbranch
fi