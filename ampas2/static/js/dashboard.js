var click_status;

// Script for date
$("datepicker").datepicker({
    isDisabled: function(date) {
        return date.valueOf() > now ? true : false;
    }
});


$(document).ready(check_local);

function set_selected_media(){
  if (localStorage.getItem("medialist")) {
    var media_list = localStorage.getItem("medialist").split(",");
    $("#medlist").val(media_list).change();
  }
}

 // Check whether the localStorage is empty or not 
function check_local(){
  select_multiple();
  if (localStorage.getItem("medshare_data") && localStorage.getItem("kol_data") && localStorage.getItem("medsum_data") && localStorage.getItem("wordfreq_data")){
    medshare_data = localStorage.getItem("medshare_data");
    kol_data = localStorage.getItem("kol_data");
    medsum_data = localStorage.getItem("medsum_data");
    wordfreq_data = localStorage.getItem("wordfreq_data");

    document.search["keyword"].value = localStorage.getItem("keyword");    
    document.search["date_start"].value = localStorage.getItem("begin");
    document.search["date_end"].value = localStorage.getItem("end");
  } 
}

function select_multiple(){
  $.when(get_media_list()).done(function(data){
    data = data.result;
    var options = [];
    $.each(data,function(c,d){
      options.push("<option value='"+d+"'>"+d+"</option>");
    });
    $("#medlist").append(options); 
    set_selected_media();
  });
  $("#medlist").select2();
}

function get_media_list(){
  return $.ajax({
    dataType: "json",
    type: "GET",
    url: create_url("listmedia"),
    crossDomain: true,
    headers:{
      "Authorization":""+set_header()
    }
  });
}

function save_session(data){
  var keyword = document.search["keyword"].value;
  var start = document.search["date_start"].value;
  var end = document.search["date_end"].value;

  if (!keyword || !start || !end){
    return false;
  }

  localStorage.setItem("keyword",keyword);
  localStorage.setItem("begin",start);
  localStorage.setItem("end",end);

  list_media = $("#medlist").val() ? $("#medlist").val() : [];
  localStorage.setItem("medialist",list_media);

  var tmp_data = JSON.stringify({
    media:list_media,
    keyword: keyword,
    begin: start+" 01:00:00",
    end: end+" 01:00:00"
  });

  localStorage.setItem("medshare_data",tmp_data);

  tmp_data = JSON.stringify({
    media:list_media,
    name: ["jokowi","prabowo","samad","sby","megawati","habibie","paloh"],
    keyword: keyword,
    begin: start+" 01:00:00",
    end: end+" 01:00:00"
  });

  localStorage.setItem("kol_data",tmp_data);

  tmp_data = JSON.stringify({
    media:list_media,
    keyword: keyword,
    begin: start+" 01:00:00",
    end: end+" 01:00:00"
  });

  localStorage.setItem("medsum_data",tmp_data);

  tmp_data = JSON.stringify({
    media:list_media,
    keyword: keyword,
    limit:20,
    begin: start+" 01:00:00",
    end: end+" 01:00:00"
  });

  localStorage.setItem("wordfreq_data",tmp_data);

  window.location.reload();
}

