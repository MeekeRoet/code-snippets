# Usage: sh convert_notebooks_to_html.sh <DIRECTORY>

foldername=$1

if [[ -d $foldername ]]; 
then
    echo "$foldername is a directory, converting recursively"
    find $foldername -name '*.ipynb' -type f -exec command jupyter nbconvert --to html {} \;
else
	echo "$foldername is not a directory";
fi