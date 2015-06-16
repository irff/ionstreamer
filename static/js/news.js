var template = $("#related-news ul");
var total_article = 0;


function show_articles(id){
	var par = "#"+id.substring(0,id.length-2)+"-par"; 
	var title = $(par).children(".title").text();
	var author = $(par).children(".author").text();
	var provider = $(par).children(".provider").text();
	var location = $(par).children(".loc").text();
	var time = $(par).children(".time").text();
	var content = $(par).children("input[type='hidden']").val();
	console.log(title);
	console.log(author);
	console.log(provider);
	console.log(location);
	console.log(time);
	console.log(content);
	var result = "";
	result += "<div class='a-t'>"+title + "</div>";
	result += "<div class='a-a'>"+author + "</div>";
	result += "<div class='a-a'>"+time+ "</div>";
	result += "<div class='a-a'>"+provider+ "</div>";
	result += "<div class='a-a'>"+location+ "</div>";
	
	result += "<p style='text-align:justify;color:#424242;'>"+content + "</p><br>";


	// $("body").attr("style","opacity:0.5;");
	modal.open({
		content: result,
		width: "600px"
	}); 
}

get_news();

function generate_result(data){	
	var list = "";
	var counter = 1;
	data.forEach(function(d){
		list += generate_item(d,counter++);
	});
	template.html(list);
}

function generate_item(data, id){
	// console.log(data);
	// console.log(data.privider);
	result = "<li  id='"+id+"-par'>";
	result = result +"<div class='title'><a id='"+id+"-t' href='#' onclick='show_articles(this.id);return false;'>"+ data.title +"</a></div>";
	result = result +"<div class='author'>by : "+ data.author +"</div>";
	result = result +"<div class='provider'>site: "+ data.provider +"</div>";
	result = result +"<div class='url'><a href='"+ data.url +"' target='_blank'>[article's link]</a>&nbsp;&nbsp;&nbsp;<a target='_blank' href='http://128.199.120.29:3000/?url="+data.url+"'>[Download snapshot]</a></div>";

	formatted = moment(data.publish);
	formatted = String(formatted._d).substring(0,25);
	result = result +"<div class='time'>time: "+ formatted +"WIB</div>";
	result = result +"<div class='loc'>location:"+ data.location +"</div>";
	result = result +"<div class='crawled' style='text-align:right;color:#212121;'>crawled on "+ String(moment(data.date_crawl)._d).substring(0,25) +"WIB</div>";
	result = result + "<input type='hidden' name='content' value='"+data.content+"'>";
	return result;
}

function get_news(){
	var from = $("#list-news").data("from");
	var size = $("#list-news").data("size");
	var data_media = localStorage.getItem("medialist").split(",").join('",').split(",").join(',"');
	var post_data = "";
    template.html('<img style="" src="/static/img/loader.gif" />');   
	if (data_media) {
		post_data = '{"media":["'+ data_media+'"],"keyword":"'+localStorage.getItem("keyword")+'","begin":"'+localStorage.getItem("begin")+' 01:00:00","end":"'+localStorage.getItem("end")+' 01:00:00","from_page":'+from+',"page_size":'+size+'}';
	} else {
		post_data = '{"keyword":"'+localStorage.getItem("keyword")+'","begin":"'+localStorage.getItem("begin")+' 01:00:00","end":"'+localStorage.getItem("end")+' 01:00:00","from_page":'+from+',"page_size":'+size+'}';
	}
	$.ajax({
	    type: 'POST',
	    // make sure you respect the same origin policy with this url:
	    // http://en.wikipedia.org/wiki/Same_origin_policy
	    url: create_url("news"),
	    data: post_data,
	    crossDomain: true,
	    success: function(msg){
	        response = msg.result[0].news;
	        total_article = msg.total;
			generate_result(response);
			$("#total-articles").html("There are "+total_article+" related articles");
			console.log(from/size);
			$('#pagination').pagination({
				pages: Math.floor(total_article/size),
				currentPage: (from/size) == 0 ? 1 : from/size,
				cssStyle: 'light-theme'
			});
	    },
        headers:{
      		"Authorization":""+set_header()
    	}
	});
}  