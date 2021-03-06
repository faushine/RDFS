# RDFS
RD means relational database. This project aims to build a filesystem on the top of MySQL.

## Installation

First, configure datasource properties in ``utils.py``.


It is easy to start the program then:
```bash
python3 rdfs.py
```

## Usage

Support various file-system utilities including ``cd, ls,
find, grep``.

For example:
```bash
$ upload
ready to traverse path: /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project
traverse success!
total files: 65
total directories 44
ready to upload contents
upload success!
$ ls
.DS_Store
.gitignore
directory.py
...
test
$ cd test
$ ls -l
-rw-r--r-- 1 faushine  staff       1 Mar 28 23:29 .DS_Store
-rw-r--r-- 1 faushine  staff       1 Mar 29 18:58 test.txt
$ grep "test" "ttt"
Find matching file: /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/test.txt
2 tttttttttt
3 tttt
$ find /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project "tes"
drwxr-xr-x     3  faushine  staff       96  Mar 29 16:19  /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/.git/refs/remotes
drwxr-xr-x     3  faushine  staff       96  Mar 29 16:19  /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/.git/logs/refs/remotes
drwxr-xr-x     4  faushine  staff      128  Mar 29 18:58  /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/test
-rw-r--r--     1  faushine  staff       50  Mar 29 18:59  /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/test.txt
-rwxr-xr-x     1  faushine  staff    28536  Apr  2 17:56  /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/testt
$ path -a
test = /Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/testt
$ path sss=/Users/faushine/Documents/CourseWork/2020Winter/ECE656/project/testt
store PATH success!

```
#### upload

Traverse the directory tree and file content in current working directory. All of files and directories will be stored in MySQL database.

#### cd

Change the current working directory.

```bash
cd [path]
```

#### ls

List files and directories in the current working directory or the specific path.


```bash
ls [-l] [path]
```

#### find

Search in the current working directory, and accept the directory and (partial) name of the file being found; output the “ls -l” results
for all matches.

```bash
find [path] [pattern]
```

#### grep

Search in the current working directory, and accept the (partial) name of the file and seek the relevant pattern in the matching file(s).
Output the line number and line for the matching lines.


```bash
grep [fpattern] [cpattern]
```
