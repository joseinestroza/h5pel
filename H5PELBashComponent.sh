#!/bin/bash

#        !This program is semi-PEP8 Compliant.

#        @author jose.inestroza@unah.edu.hn,joseinestroza.developer@outlook.com
#        @version 0.1.0p
#        @date 2021/11/19

#        !H5PEL Bash Component: H5PEL Language Packager (H5P Easy 
#        !Language) for ".H5P" file creation.
#        Copyright (C) 2021  José Inestroza
#        !Created at Tegucigalpa, Honduras, C.A.

#        This program is free for charge software: you can share it (copy and redistribute 
#        the material in any medium or format) and/or modify it (remix, 
#        transform, and build upon the material) under the terms of
#        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0), 
#        under the following terms:

#        #        Attribution — You must give appropriate credit, provide a link to the 
#        #        license, and indicate if changes were made. You may do so in any reasonable 
#        #        manner, but not in any way that suggests the licensor endorses you or your use.

#        #        NonCommercial — You may not use the material for commercial purposes.

#        #        ShareAlike — If you remix, transform, or build upon the material, you 
#        #        must distribute your contributions under the same license as the original.

#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY. 

#        https://creativecommons.org/licenses/by-nc-sa/4.0/

#        !This project depends on Lark Parser. See Lark Parser Licence for more information.

#        https://github.com/lark-parser/lark/blob/master/LICENSE

clear;

#Resources
RESOURCEPATH="Resources"
TEMPFILENAME="temp.temp"
H5PFILENAMEPATH="$RESOURCEPATH/$TEMPFILENAME"

#Create H5PEL content and configuration files
cat $1 | python3 H5PELPythonComponent.py

#Reads dynamic H5PEL final name file
H5PFILENAME=`cat $H5PFILENAMEPATH`

#Final file name date
DATE=`date '+%Y'-'%m'-'%d'-'%H'-'%M'-'%S'`
DATE="_$DATE"

#ZIP File creation inside Resource directory
cd $RESOURCEPATH
rm -f $TEMPFILENAME
zip -r -D -X $H5PFILENAME *

#Moves filnal result outside Resource directory
mv $H5PFILENAME ../
cd ..

#Done
echo "Done: $H5PFILENAME"