var monthnum = month();
var year = year();

//Meget af koden i dette script er blevet beskrevet i script.js, dette scripts opgave er at finde dags dato og omdirigere
//til en side med datoen i URL'en

function month(){
    var d = new Date();
	var dato = d.toDateString();
	var res = dato.split(' ');
    var month = res[1];
    if (month == 'Jan'){ var monthnum = 0}
    if (month == 'Feb'){ var monthnum = 1}
    if (month == 'Mar'){ var monthnum = 2}
    if (month == 'Apr'){ var monthnum = 3}
    if (month == 'May'){ var monthnum = 4}
    if (month == 'Jun'){ var monthnum = 5}
    if (month == 'Jul'){ var monthnum = 6}
    if (month == 'Aug'){ var monthnum = 7}
    if (month == 'Sep'){ var monthnum = 8}
    if (month == 'Oct'){ var monthnum = 9}
    if (month == 'Nov'){ var monthnum = 10}
    if (month == 'Dec'){ var monthnum = 11}
    var monthnum = parseInt(monthnum);
    return monthnum;
}

function year(){
    var d = new Date();
	var dato = d.toDateString();
	var res = dato.split(' ');
	var year = res[3];
	var year = parseInt(year);
	return year;
}

function start_date(){
    var d = new Date();
    var dato = d.toDateString();
    var res = dato.split(' ');
    var date = res[2];
    var date = parseInt(date);
    document.getElementById(date).innerHTML = '<span class="active">' + date + '</span>';
    window.location = "/calender?day=" + date + "&month=" + monthnum + "&year=" + year;
}