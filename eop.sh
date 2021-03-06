#!/bin/bash 
N=$#

if [ $# -eq 0 ]; then 
    echo -e  "You need to supply a date. This can be in either Julian Day, year & DOY or year and date format.\nUsage: ./get_eops.utas.sh 2456146\nOR ./get_eops.utas.sh 2012 220\nOR ./get_eops.utas.sh 2012 8 7"
    exit
elif [ $# -eq 1 ]; then #assume it is a julian day number
    echo $(($1-1)) > /tmp/jd
elif [ $# -eq 2 ]; then 
    cd /home/observer/fc_auscope
echo "[month,day]=doy2date($1, $2-1);FID=fopen('/tmp/jd', 'w');fwrite(FID, mat2str(real( floor(julday1([day month $1 0])))));fclose(FID)"  | octave > /dev/null 2> /dev/null
elif [$# -eq 3 ]; then
cd /home/observer/fc_auscope
echo "FID=fopen('/tmp/jd', 'w');fwrite(FID, mat2str(real( floor(julday1([$3 $2 $1 0])))));fclose(FID)"  | octave > /dev/null 2> /dev/null
jd=$(cat /tmp/jd)
echo $(($fd-1)) > /tmp/jd
fi

cd /tmp/
#wget -N ftp://cddis.gsfc.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/usno_finals.erp
curl --insecure -O --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/usno_finals.erp
cp usno_finals.erp usno_finals.erp2
cat usno_finals.erp2  | tr -s ' ' > usno_finals.erp

if [ $1 -lt 2017 ]  ; then 

for i in 1 2 3 4 5 ; do
echo "EOP $(echo "$( grep -A 5  $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 1)-2400000.5" | bc | cut -d '.' -f 1) { xPole=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 2)/10 " | bc) yPole=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 3)/10 " | bc) tai_utc=36 ut1_utc=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 |tr -s ' ' | cut -d ' ' -f 4)/1000000 +36"  | bc ) }" 
done
#

else

for i in 1 2 3 4 5 ; do
echo "EOP $(echo "$( grep -A 5  $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 1)-2400000.5" | bc | cut -d '.' -f 1) { xPole=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 2)/10 " | bc) yPole=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 | tr -s ' ' | cut -d ' ' -f 3)/10 " | bc) tai_utc=37 ut1_utc=$(echo "scale=6;$(grep -A 5 $(cat /tmp/jd).5 usno_finals.erp | head -$i | tail -1 |tr -s ' ' | cut -d ' ' -f 4)/1000000 +37"  | bc ) }"
done

fi
