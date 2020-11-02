var monthnum = month();
var year = year();
var d = new Date(); //Skaffer dags dato i formatet: Dag, Måned, Dato, År, Klokken, Tidszone, Tidszonens lokalisation
var dato = d.toDateString(); //Laver datoen om til en string
var res = dato.split(' '); //splitter datoen ved mellemrum, så vi får informationerne hver for sig i en liste
var date = res[2]; //Hiver datoen ud fra listen
var day = day();
var chosen_day = parseInt(date); //Laver en variabel med datoen som integer, i stedet for string

function month(){
    var url =  window.location.href //skaffer ULR'en for siden
    var month = /month=([^&]+)/.exec(url)[1]; // Går igennem url'ens parametre og ser om der en noget det matcher "month=([^&]+)", hvis der er, så retunerer den resultatet
    var month = month ? month : 'myDefaultValue'; //Retunerer 'myDefaultValue', hvis month ikke eksisterer
    var month = parseInt(month); //Laver månednummeret om til en interger
    return month
} // credit: http://stackoverflow.com/questions/979975/how-to-get-the-value-from-the-get-parameters

function year(){ //Fungerer på samme måde som month()
    var url =  window.location.href
    var year = /year=([^&]+)/.exec(url)[1];
    var year = year ? year : 'myDefaultValue';
    var year = parseInt(year);
    return year
} // credit: http://stackoverflow.com/questions/979975/how-to-get-the-value-from-the-get-parameters

function day(){ //Fungerer på samme måde som month()
    var url =  window.location.href
    var day = /day=([^&]+)/.exec(url)[1];
    var day = day ? day : 'myDefaultValue';
    var day = parseInt(day);
    return day
} // credit: http://stackoverflow.com/questions/979975/how-to-get-the-value-from-the-get-parameters

function show_month_and_year(){ //I Javascript er Januar den 0. måned og December den 11.
    if (monthnum == 0){ var month2 = 'Januar';} //Opretter en variabel med månedens navn, ud fra nummeret
    if (monthnum == 1){ var month2 = 'Februar';}
    if (monthnum == 2){ var month2 = 'Marts';}
    if (monthnum == 3){ var month2 = 'April';}
    if (monthnum == 4){ var month2 = 'Maj';}
    if (monthnum == 5){ var month2 = 'Juni';}
    if (monthnum == 6){ var month2 = 'Juli';}
    if (monthnum == 7){ var month2 = 'August';}
    if (monthnum == 8){ var month2 = 'September';}
    if (monthnum == 9){ var month2 = 'Oktober';}
    if (monthnum == 10){ var month2 = 'November';}
    if (monthnum == 11){ var month2 = 'December';}
    document.getElementById("month").innerHTML = month2 + '<br><span id="year" style="font-size:18px">' + year + '</span>'; //Viser måned og år på siden
}

function next(){ //Går frem til næste måned
    if (monthnum < 11){
    monthnum +=1;} //Hvis man ikke er i den sidste måned af året, vil den lægge 1 til månednumeret
    else if (monthnum == 11){
    monthnum = 0;
    year +=1;} //Hvis man befinder sig i den sidste måned, går den til den første måned og et år frem
    show_month_and_year(); //Opdaterer måneden og året, der er vist i toppen
    start_day(); //Opdaterer startdagen for måneden
    number_of_days(); //Opdaterer antallet af dage i måneden
    var day = 1;
    window.location = "/calender?day=" + day + "&month=" + monthnum + "&year=" + year; //Opdaterer siden
}

function prev(){
    if (monthnum > 0){
    monthnum -=1;}
    else if (monthnum == 0){
    monthnum = 11;
    year -= 1;}
    show_month_and_year();
    start_day();
    number_of_days();
    var day = 1;
    window.location = "/calender?day=" + day + "&month=" + monthnum + "&year=" + year;
} //Fungerer med samme princip som next(), men bare bagud

function start_day(){ //Finder hvilken dag måneden starter med, og fylder det ind i kalenderen
    var dd = new Date(parseInt(year),monthnum,1), //Opretter en dato variabel for det nuværende år, nuværende måned og d. 1. dag i måneden
        strdd = dd.toDateString(), //Laver datoen om til en streng
        listday1 = strdd.split(' '); //Splitter strengen op
    document.getElementById("day1").innerHTML = listday1[0]; //Ændrer den 1. dag i kalenderen til den 1. dag i måneden

    var dd = new Date(parseInt(year),monthnum,2),
        strdd = dd.toDateString(),
        listday2 = strdd.split(' ');
    document.getElementById("day2").innerHTML = listday2[0]; //Ændrer den 2. dag i kalenderen til den 2. dag i måneden

    var dd = new Date(parseInt(year),monthnum,3),
        strdd = dd.toDateString(),
        listday3 = strdd.split(' ');
    document.getElementById("day3").innerHTML = listday3[0];//Ændrer den 3. dag i kalenderen til den 3. dag i måneden

    var dd = new Date(parseInt(year),monthnum,4),
        strdd = dd.toDateString(),
        listday4 = strdd.split(' ');
    document.getElementById("day4").innerHTML = listday4[0];//Ændrer den 4. dag i kalenderen til den 4. dag i måneden

    var dd = new Date(parseInt(year),monthnum,5),
        strdd = dd.toDateString(),
        listday5 = strdd.split(' ');
    document.getElementById("day5").innerHTML = listday5[0];//Ændrer den 5. dag i kalenderen til den 5. dag i måneden

    var dd = new Date(parseInt(year),monthnum,6),
        strdd = dd.toDateString(),
        listday6 = strdd.split(' ');
    document.getElementById("day6").innerHTML = listday6[0];//Ændrer den 6. dag i kalenderen til den 6. dag i måneden

    var dd = new Date(parseInt(year),monthnum,7),
        strdd = dd.toDateString(),
        listday7 = strdd.split(' ');
    document.getElementById("day7").innerHTML = listday7[0];//Ændrer den 7. dag i kalenderen til den 7. dag i måneden
}

function number_of_days(){  //Som udgangspunkt er der sat 31 dage ind i hver måned, denne funktion fjerner så de
    if (monthnum == 1){     //de overskydende dage, i de måndeder, hvor der ikke er 31 dage.
    document.getElementById("29").innerHTML = "";
    document.getElementById("30").innerHTML = "";
    document.getElementById("31").innerHTML = "";
    if (year % 4 === 0){ //Tjekker om årstallet kan divideres med 4 ( skudår ) og sætter en ekstra dag ind
    document.getElementById("30").innerHTML = "";
    document.getElementById("31").innerHTML = "";}}
    if (monthnum == 3){
    document.getElementById("31").innerHTML = "";}
    if (monthnum == 5){
    document.getElementById("31").innerHTML = "";}
    if (monthnum == 8){
    document.getElementById("31").innerHTML = "";}
    if (monthnum == 10){
    document.getElementById("31").innerHTML = "";}
    if (day < 10){
    document.getElementById(day).innerHTML = '<span class="active2">' + day + '</span>';}
    else {
    document.getElementById(day).innerHTML = '<span class="active">' + day + '</span>';} //Markerer den dag man befinder sig på
}

function shown_day(chosen){
    window.location = "/calender?day=" + chosen + "&month=" + monthnum + "&year=" + year; //Tager dagen, måneden og året man befinder sig på
    chosen_day = chosen;                                                                  //og omdirigerer til en URL med disse oplysninger i
}

function today(){ //omdirigerer til dags dato
    var d = new Date(),
	dato = d.toDateString(),
	res = dato.split(' '),
	today = res[2],
	tomonth = res[1],
	toyear = res[3];
	if (tomonth == 'Jan'){ var tomonth = 0}
    if (tomonth == 'Feb'){ var tomonth = 1}
    if (tomonth == 'Apr'){ var tomonth = 3}
    if (tomonth == 'Mar'){ var tomonth = 2}
    if (tomonth == 'May'){ var tomonth = 4}
    if (tomonth == 'Jun'){ var tomonth = 5}
    if (tomonth == 'Jul'){ var tomonth = 6}
    if (tomonth == 'Aug'){ var tomonth = 7}
    if (tomonth == 'Sep'){ var tomonth = 8}
    if (tomonth == 'Oct'){ var tomonth = 9}
    if (tomonth == 'Nov'){ var tomonth = 10}
    if (tomonth == 'Dec'){ var tomonth = 11}
    window.location = "/calender?day=" + today + "&month=" + tomonth + "&year=" + toyear;
}

function key_event() { //Skifter måned når venstre- eller højre piltast bliver trykket ned.
    var key = event.keyCode; //Får koden for tasten man trykker ned
	if (key == 37){ //Hvis man trykker på venstre piltast kører den prev()
	prev();
	}
	else if (key == 39){ //Hvis man trykker på højre piltast kører den next()
	next();
	}
}