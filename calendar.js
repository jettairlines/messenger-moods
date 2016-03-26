function calendar() {
	
	data.forEach(function(e){
		e.date = new Date(e.date);
		e.date.setHours(0,0,0,0);
	});
	data.sort(function(a, b) {
    	return a.date - b.date;
	});
	
	var it = 0;
//	var record = $();
	for (var d = data[0].date; d <= data[data.length-1].date; d.setUTCDate(d.getUTCDate() + 1) ) {
//		if(it==data.length) break;

//		console.log(it);
		if(d.toLocaleDateString() === data[it].date.toLocaleDateString() ){
			drawDay(data[it]);
			it++;
			//		console.log(d.toLocaleDateString() + ' ' + data[it].date.toLocaleDateString());
		}
		else
			$("#canvas").append("<div class='date'></div>");
	}
	drawDay(data[data.length-1]);
}


function drawDay(day){
	var thisDay = $("<div class='date'></div>");
	if(day.mood == "pos")
		thisDay.addClass("pos");
	else if(day.mood == "neg")
		thisDay.addClass("neg");
	else if(day.mood == "compound")
		thisDay.addClass("comp");
	
	$("#canvas").append(thisDay);
}



