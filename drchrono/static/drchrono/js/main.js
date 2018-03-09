function startTime(s=-1) {
	var today = new Date();
	if(s==-1){
    	ch = today.getHours() * 3600;
        cm = today.getMinutes() * 60;
        cs = today.getSeconds() + cm + ch;
    };

    var h = today.getHours() * 3600;
    var m = today.getMinutes() * 60;
    var s = today.getSeconds() + m + h;

    document.getElementById('txt').innerHTML =
    Math.floor((s - cs) / 3600) + ":" + Math.floor((s - cs) / 60) + ":" + (s - cs);
    var t = setTimeout(startTime, 100, cs);
}
