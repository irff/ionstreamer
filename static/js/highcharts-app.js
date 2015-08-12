$(function(){
  var spin = '<h1><i class="fa fa-lg fa-spinner fa-spin"></i></h1>';
  function drawFreq() {
    $("#freq").html(spin);
    $.get('/api/analyze/freq/'+encodeURIComponent($('#keyword').text()), function(r){
      var positive = r.reduce(function(acc, curr){return acc + curr[2];}, 0);
      var negative = r.reduce(function(acc, curr){return acc + curr[3];}, 0);
      $('#freq').highcharts('StockChart', {
        credits: {enabled: false},
        legend: {enabled: true, shadow: true},
        title: {text: "Growth of Tweet"},
        colors: ['#EE0000', '#00EE00', '#4099FF'],
        series: [
          {
            name: 'Negative Tweets',
            // marker: { enabled: true, radius: 2 },
            shadow: true,
            data: r.map(function(x){return [x[0], x[3]]})
          },
          {
            name: 'Positive Tweets',
            // marker: { enabled: true, radius: 2 },
            shadow: true,
            data: r.map(function(x){return [x[0], x[2]]})
          },
          {
            name: 'All Tweets',
            // marker: { enabled: true, radius: 2 },
            shadow: true,
            data: r.map(function(x){return [x[0], x[1]]})
          },
        ],
        navigator: {baseSeries: 2},
        rangeSelector: {
          buttons: [
            {type: 'hour', count: 6, text: '6h'},
            {type: 'hour', count: 12, text: '12h'},
            {type: 'day', count: 1, text: '1d'},
            {type: 'day', count: 7, text: '7d'},
            {type: 'month', count: 1, text: '1m'},
            {type: 'all', text: 'All'}
          ]
        },
        xAxis: { type: "datetime", },
        yAxis: {
          title: {text: "Number of Tweet"},
          allowDecimals: false,
          ordinal: false,
          startOnTick: false,
          // maxPadding: 0.2,
          minPadding: 0.2,
        },
        tooltip: {borderColor: 'silver'},
      });

      $("#sentiment").html(spin);
      $('#sentiment').highcharts({
        credits: {enabled: false},
        legend: {enabled: true, shadow: true},
        title: {text: "Sentiment Analytics"},
        colors: ['#EE0000', '#00EE00'],
        tooltip:
        {
          formatter: function() {
            return "<strong>" + this.y + "</strong> "+ this.point.name +" tweets"
          },
        },
        series: [
          {
            type: 'pie',
            name: "Number of Tweet",
            allowPointSelect: true,
            cursor: 'pointer',
            startAngle: 90,
            dataLabels: {enabled: true},
            showInLegend: true,
            shadow: true,
            data: [
              {
                name: "negative",
                y: negative
              },
              {
                name: "positive",
                y: positive
              },
            ],
            dataLabels: {format: '{point.percentage:.2f} %',},
          },
        ],
      });
    }, 'JSON');
  }

  function drawTopMention() {
    $("#topmention").html(spin);
    $.get('/api/analyze/topmention/'+encodeURIComponent($('#keyword').text()), function(r){
      $('#topmention').highcharts({
        credits: {enabled: false},
        chart: {type: 'bar'},
        title: {text: "Top Mention People",},
        colors: ['#4099FF'],
        legend: {enabled: false},
        series: [
          {
            name: "Top Mention People",
            shadow: true,
            data: r
          }
        ],
        tooltip:
        {
          formatter: function(){
            return "<strong>" + this.y + "</strong> mentions to <strong>" + this.x + "</strong>"
          },
        },
        xAxis:
        {
          title: {text: "People"},
          categories: r.map(function(x){return x[0]})
        },
        yAxis:
        {
          maxPadding: 0,
          title: {text: "Number of Mention"},
        }
      });
      setTimeout(drawFreq, 1000);
    }, 'JSON');
  }

  function drawTopPosting() {
    $("#topposting").html(spin);
    $.get('/api/analyze/topposting/'+encodeURIComponent($('#keyword').text()), function(r){
      $('#topposting').highcharts({
        credits: {enabled: false},
        chart: {type: 'bar'},
        title: {text: "Top Posting",},
        colors: ['#4099FF'],
        legend: {enabled: false},
        series: [
          {
            name: "Top Posting",
            shadow: true,
            data: r
          }
        ],
        tooltip:
        {
          formatter: function(){
            return "<strong>" + this.y + "</strong> tweets from <strong>" + this.x + "</strong>"
          },
        },
        xAxis:
        {
          title: {text: "People"},
          categories: r.map(function(x){return x[0]})
        },
        yAxis:
        {
          maxPadding: 0,
          title: {text: "Number of Posting"},
        }
      });
      setTimeout(drawTopMention, 1000);
    }, 'JSON');
  }

  drawTopPosting();
  
});