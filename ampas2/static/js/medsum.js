window.onload = init_chart();

Array.prototype.indexOfNested = function(str){
  for (var i=0;i<this.length;++i){
    if (this[i][0] === str)
      return i;
  }
  return -1;
}

function init_chart(){
  if (localStorage.getItem("medsum_data")) {
    $("#result").html('<img class="loader" src="/static/img/loader.gif" />');
  }
  $.when(get_mediasummary()).done(function(b){
    make_piechart(prettify_summary_data(b.result[0].media), '#result', 'Media Summary');
  });
}

function get_mediasummary(){
  return $.ajax({
      type: 'POST',
      url: create_url("/mediashare/summary"),
      data: localStorage.getItem("medsum_data"),
      headers : {	
        "Authorization":set_header()
      }
  });
}

function prettify_summary_data(data){
  result = [];
  console.log(data);
  Object.keys(data).forEach(function(d){
    result.push([d,data[d]]);
  });

  return result;
}

function make_piechart(data, div, desc){
  var chart = c3.generate({
    bindto :div,
    size : {
      width: $(window).width(),
      height: 400
    },
    padding: {
      top: 0
    },
    data : {
      columns : data,
      type : 'donut'
    },
    donut: {
        title: desc,
        label: {
            format: function (value, ratio, id) {
                // console.log(value+" "+ratio+" "+id);
                return value;
            }
        }
    }
  });
}
