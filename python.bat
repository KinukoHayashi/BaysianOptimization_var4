
echo "start, bat!"
echo "%1 = " %1
echo "%2 = " %2

"C:\Program Files\Altair\2021.1\EDEM2021.1\bin\edem.exe" -c -i "D:/hayashi_dem/drum_dem_test6/test6_"+%1+".dem" -R
if exist test.txt goto :th


:th
echo "end, bat!"

