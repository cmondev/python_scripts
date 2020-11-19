# Filter and copy

### The basic idea
This script was originally created to perform a flat copy of pictures 
downloaded from Google Photos. The downloaded zip archive(s) have following 
structure (file names are german):  
  
    .
    |-- Google Fotos
    |   |-- 11.11.2011
    |   |   |-- Metadaten.json
    |   |   |-- 133719_931.jpg.json
    |   |   |-- 133719_931.jpg
    |   |   |-- 859033_224.jpg.json
    |   |   |-- 859033_224.jpg
    |   |   |-- 859033_224-bearbeitet.jpg
    |   |-- 12.11.2011
    |   |   |-- Metadaten.json
    |   |   |-- ...
    |   |-- ...                            

So what I wanted to achieve is to traverse all folders and filter for all files with
extension *.jpg. Furthermore if there is a file which name includes "bearbeitet" 
(german for "edited") I want to keep this file, but skip the original file. 

### How to use the script
Following options are possible.

    -h, --help              show this help message and exit
    -d, --dry               Dry run. Affected files will be logged, but no files
                            will be copied
                            
    -e [EXTENSION [EXTENSION ...]], --extensions [EXTENSION [EXTENSION ...]]
                            The file extension to filter with, e.g. -e *.jpg.
                            Default is .* for all file extensions. Can also be a
                            list, e.h. -e *.jpg *.png
                            
    -f FILTERSTRING, --filter FILTERSTRING
                            Filter string to search for if duplicates are to be
                            expected. For example A.pdf will be ignored and
                            A_edited.pdf will be kept if -f _edited
                            
    -o OUTPUT, --output OUTPUT
                            Output folder to copy files to. Either absolute or
                            relative.
                            
    -s SOURCE, --source SOURCE
                            Source folder to check. Either absolute or relative.

Either -e or -f has to be set. So the example command for for my Google Photos 
usecase looks like this (assuming I am currently in the root folder of the structure 
shown above):

    python fac.py -e *.jpg -f="-bearbeitet" -o output
    
You can see since the filter string "-bearbeitet" contains a dash, it has to be quoted 
and a "=" has to be used. This is due to python's built-in argsparse.
