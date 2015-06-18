window.onload = init_chart();

Array.prototype.indexOfNested = function(str){
  for (var i=0;i<this.length;++i){
    if (this[i][0] === str)
      return i;
  }
  return -1;
}

function init_chart(){
  if (localStorage.getItem("wordfreq_data")) {
    $("#result").html('<img class="loader" src="/static/img/loader.gif" />');
  }

  $.when(get_wordfrequency()).done(function(d){
    make_barchart(prettify_frequency_data(d.result[0].words),get_category(d.result[0].words));
  });
}

function get_wordfrequency(){
  return $.ajax({
      type: 'POST',
      url: create_url("wordfrequencymanual"),
      data: localStorage.getItem("wordfreq_data"),
      headers: {
        "Authorization":set_header()
      }
  });   
}

function prettify_frequency_data(data){
  result = ["Word Frequency"];
  Object.keys(data).forEach(function(d){
    result.push(data[d]);
  });
  return result;
}

function get_category(data){
  result = [];
  Object.keys(data).forEach(function(d){
    result.push(d);
  });
  return result;
}

function make_barchart(data,cat){
  var chart = c3.generate({
      bindto : '#result',
      padding: {
        top: 0
      },
      data: {
          columns: [
              data,
          ],
          type: 'bar'
      },
      bar: {
          width: {
              ratio: 0.5
          }
      },
      axis : {
        x : {
          type: 'category',
          categories : cat,
          label: {
            text: "20 kata terbanyak",
          }
        },
        y : {
          label: {
            text: "Jumlah kata"
          }
        }
      }
  });
}
