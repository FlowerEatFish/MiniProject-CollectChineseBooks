![project][1] ![license][2]

[1]: https://img.shields.io/badge/project-privacy-red.svg
[2]: https://img.shields.io/badge/license-no%20license-blue.svg
***

## Introduction:

It is used for searching information of chinese book from a Taiwan website called [NBINET](http://nbinet3.ncl.edu.tw/screens/opacmenu_cht.html), and create an excel file.

> 2017-02-14
>
> Initially, I just built it to help me with repetitive work.
>
> 2017-09-14
>
> It has been completed for the construction of my request, but I will continue construct it better.

***

> #### [No License](https://choosealicense.com/no-license/):
>
> Everybody is forbidden to use, copy, distribute, and modify the project except contributors.

***

> #### Requests:
>
> Python v3.5.*
>
> openpyxl v2.4.*
>
> beautifulsoup4 v4.*

***

> #### Porject Flows:
>
> 1. Read Microsoft Office Excel file.
>
> 2. Catch ISBN from Excel file.
>
> 3. Collect book details from NBINET via ISBN.
>
> 4. Search special library for obtaining better book details.
>
> 5. Write book details into Excel file.

***

> #### Progress:
>
> - [x] Manual find the path of .xlsx file.
>
> - [x] Read .xlsx file.
>
> - [x] Auto detect the amount of the books from .xlsx file.
>
> - [x] Catch ISBN in .xlsx file.
>
> - [ ] Determine the book format (MARC21 or Chinese MARC).
>
> - [x] Search special library for obtaining better book details.
>
> - [ ] Return null value if ISBN is invalid.
>
> - [x] Collect book details from NBINET.
>
> - [ ] Check progress on terminal.
>
> - [x] Write .xlsx file.
