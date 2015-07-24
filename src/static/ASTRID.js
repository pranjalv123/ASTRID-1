function connect() {
    server = $("#server")[0].value;
    port = $("#port")[0].value;
    console.log(jQuery.get("http://" + server + ":" + port + "/ping/"));
}

function start() {

    method = $('input[name="method"]:checked').val();

    var formdata = new FormData();

    formdata.append("method", method);

    var file = $('#genetrees')[0].files[0]

    formdata.append("genetrees", file)
    
    console.log(formdata);

    $.ajax({
	url:'/start',
	data:formdata,
	cache: false,
	contentType: false,
	processData: false,
	type:'POST',
	success: function(data) {
	    jobid = data;
	    updater = window.setInterval(function() { updatestatus() }, 500 )
	}});

}

function updatestatus() {
    $.ajax({
	data:{'jobid':jobid},
	url:'/status',
	type:'GET',
	success:function(json) {
	    data = JSON.parse(json);
	    console.log(data);
	    if (data['status'] == 'done') {
		$("#progbar")[0].value = 1;
		$("#progressbar")[0].style.display = "none";
		$("#tree")[0].innerHTML = data['tree'];
		$("#status")[0].innerHTML = "Done!";
		window.clearInterval(updater);
	    } else {
		if (data['pct'] > 0 && data['pct'] < 1) {
		    $("#progressbar")[0].style.display = "block";
		}
		$("#status")[0].innerHTML = data['status'];
		$("#progbar")[0].value = data['pct'];
	    }
	    
	}})   
}
