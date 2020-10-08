printf "pages:\t\t"
ls -r data/pages/20* 2> /dev/null | wc -l
printf "sentiment:\t"
ls -r data/sentiment/20* 2> /dev/null | wc -l
printf "pages-es:\t"
ls -r data/pages-es/20* 2> /dev/null | wc -l
printf "pages-tr:\t"
ls -r data/pages-tr/20* 2> /dev/null | wc -l
printf "sentiment-es:\t"
ls -r data/sentiment-es/20* 2> /dev/null | wc -l
