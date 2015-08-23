$(function(){

  Highcharts.setOptions({
    global: {timezoneOffset: -420}
  });

  var spin = '<h1><i class="fa fa-lg fa-spinner fa-spin"></i></h1>';

  var updateFreqChart = function(r) {
    $('#freq').highcharts('StockChart', {
      credits: {enabled: false},
      legend: {enabled: true, shadow: true},
      title: {text: "Growth of Tweet"},
      colors: ['#A9A9A9', '#DDDD00', '#DD0000', '#00DD00', '#4099FF'],
      series: [
        {name: 'Uninformative Tweet', shadow: true, visible: false, data: r.map(function(x){return [x[0], x[5]]}) },
        {name: 'Neutral Tweet', shadow: true, visible: false, data: r.map(function(x){return [x[0], x[4]]}) },
        {name: 'Negative Tweet', shadow: true, visible: false, data: r.map(function(x){return [x[0], x[3]]}) },
        {name: 'Positive Tweet', shadow: true, visible: false, data: r.map(function(x){return [x[0], x[2]]}) },
        {name: 'All Tweet', shadow: true, data: r.map(function(x){return [x[0], x[1]]}) },
      ],
      navigator: {baseSeries: 4},
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
        minPadding: 0.2,
      },
      tooltip: {borderColor: 'silver'},
      plotOptions: {
        series: {
          cursor: 'pointer',
          events: {
            click: function (event) {
              var keyword = $("#keyword").text();
              var t1 = new Date(event.point.x);
              var itv = this.points[1].x - this.points[0].x;
              var t2 = new Date(event.point.x + itv);
              kelas = 2 - event.point.series.index;
              angular.element('#analyzeController').scope().fetchTweetsAt($('#keyword').text(), kelas, t1.toISOString(), t2.toISOString());
              angular.element('#analyzeController').scope().$applyAsync();
              $('#tweets').foundation('reveal', 'open');
            }
          },
          dataGrouping: {approximation: "sum", enabled: true, }
        },
      },
    });

    var positive = r.reduce(function(acc, curr){return acc + curr[2];}, 0);
    var negative = r.reduce(function(acc, curr){return acc + curr[3];}, 0);
    var neutral = r.reduce(function(acc, curr){return acc + curr[4];}, 0);
    var dummy = r.reduce(function(acc, curr){return acc + curr[5];}, 0);

    $('#sentiment').highcharts({
      credits: {enabled: false},
      legend: {enabled: true, shadow: true},
      title: {text: "Sentiment Analytics"},
      colors: ['#A9A9A9', '#DDDD00', '#DD0000', '#00DD00'],
      tooltip:
      {
        formatter: function() {
          return "<strong>" + this.y + "</strong> "+ this.point.name
        },
      },
      series: [
        {
          type: 'pie',
          name: "Number of Tweet",
          allowPointSelect: true,
          cursor: 'pointer',
          size:"75%",
          dataLabels: {enabled: true},
          showInLegend: true,
          shadow: true,
          data: [
            {name: "Uninformative Tweet", y: dummy },
            {name: "Neutral Tweet", y: neutral },
            {name: "Negative Tweet", y: negative },
            {name: "Positive Tweet", y: positive },
          ],
          dataLabels: {format: '{point.percentage:.2f}%',},
        },
      ],
    });

    /*console.log(self);

    drawTopMention();
    drawTopPosting();
    drawTopHashtag();
    drawTopURL();*/

  };

  var updateTopMentionChart = function( r ) {
    $('#topmention').highcharts({
      credits: {enabled: false},
      chart: {type: 'bar'},
      title: {text: "Top Mention People",},
      colors: ['#4099FF'],
      legend: {enabled: false},
      series: [{name: "Top Mention People", shadow: true, data: r} ],
      tooltip:
      {
        formatter: function(){return "<strong>" + this.y + "</strong> mentions to <strong>" + this.key + "</strong>"},
        followPointer: true,
      },
      xAxis: {title: {text: "People"}, type: "category", },
      yAxis: {maxPadding: 0, title: {text: "Number of Mention"}, },
      plotOptions: {
        series: {
          cursor: 'pointer',
          events: {
            click: function (event) {
              var keyword = $("#keyword").text();
              var username = event.point.name;
              angular.element('#analyzeController').scope().fetchTweetsTo(keyword, username);
              angular.element('#analyzeController').scope().$applyAsync();
              $('#tweets').foundation('reveal', 'open');
            }
          }
        },
      },
    });
  };

  var updateTopPostingChart = function( r ) {
    $('#topposting').highcharts({
      credits: {enabled: false},
      chart: {type: 'bar'},
      title: {text: "Top Posting",},
      colors: ['#4099FF'],
      legend: {enabled: false},
      series: [{name: "Top Posting", shadow: true, data: r } ],
      tooltip:
      {
        formatter: function(){return "<strong>" + this.y + "</strong> tweets from <strong>" + this.key + "</strong>"; },
        followPointer: true,
      },
      xAxis: {title: {text: "People"}, type: "category", },
      yAxis: {maxPadding: 0, title: {text: "Number of Posting"}, },
      plotOptions: {
        series: {
          cursor: 'pointer',
          events: {
            click: function (event) {
              var keyword = $("#keyword").text();
              var username = event.point.name;
              angular.element('#analyzeController').scope().fetchTweetsFrom(keyword, username);
              angular.element('#analyzeController').scope().$applyAsync();
              $('#tweets').foundation('reveal', 'open');
            }
          }
        },
      },
    });
  };

  var updateTopHashtagChart = function( r ) {
    $('#tophashtag').highcharts({
      credits: {enabled: false},
      chart: {type: 'bar'},
      title: {text: "Top Hashtag",},
      colors: ['#4099FF'],
      legend: {enabled: false},
      series: [{name: "Top Hashtag", shadow: true, data: r } ],
      tooltip:
      {
        formatter: function(){return "<strong>" + this.y + "</strong> tweets about <strong>" + this.key + "</strong>"; },
        followPointer: true,
      },
      xAxis: {title: {text: "Hashtag"}, type: "category", },
      yAxis: {maxPadding: 0, title: {text: "Number of Hashtag"}, },
      plotOptions: {
        series: {
          cursor: 'pointer',
          events: {
            click: function (event) {
              var keyword = $("#keyword").text();
              var hashtag = event.point.name;
              angular.element('#analyzeController').scope().fetchTweetsHashtag(keyword, hashtag);
              angular.element('#analyzeController').scope().$applyAsync();
              $('#tweets').foundation('reveal', 'open');
            }
          }
        },
      },
    });
  };

  var updateTopURLChart = function( r ) {
    $('#topurl').highcharts({
      credits: {enabled: false},
      chart: {type: 'bar'},
      title: {text: "Top URL",},
      colors: ['#4099FF'],
      legend: {enabled: false},
      series: [{name: "Top URL", shadow: true, data: r } ],
      tooltip:
      {
        formatter: function(){return "<strong>" + this.y + "</strong> tweets contains <strong>" + this.key + "</strong>"; },
        followPointer: true,
      },
      xAxis: {
        title: {text: "URL"},
        type: "category",
        labels: {formatter: function() {return this.value.substr(this.value.indexOf('://')+3,16); }, },
      },
      yAxis: {maxPadding: 0, title: {text: "Number of URL"}, },
      plotOptions: {
        series: {
          cursor: 'pointer',
          events: {
            click: function (event) {
              var url = event.point.name;
              window.open(url,'_newtab');
            }
          }
        },
      },
    });
    $("#topretweet").click();
    $("#randomtweet").click();
  };

  var showTryAgain = function(id, onclick) {
    $(id).html('<button class="label alert radius" onclick="'+onclick+'">Try Again</button>');
  };

  drawFreq = function() {
    $("#freq").html(spin);
    $.ajax({
      url: '/api/analyze/freq/'+encodeURIComponent($('#keyword').text()),
      success: updateFreqChart,
      error: function(){ showTryAgain("#freq", "drawFreq()"); },
      dataType: 'json',
    });
    return self;
  };

  drawTopMention = function() {
    $("#topmention").html(spin);
    $.ajax({
      url: '/api/analyze/topmention/'+encodeURIComponent($('#keyword').text()),
      success: updateTopMentionChart,
      error: function(){ showTryAgain("#topmention", "drawTopMention()"); },
      dataType: 'json',
    });
    return self;
  };

  drawTopPosting = function() {
    $("#topposting").html(spin);
    $.ajax({
      url: '/api/analyze/topposting/'+encodeURIComponent($('#keyword').text()),
      success: updateTopPostingChart,
      error: function(){ showTryAgain("#topposting", "drawTopPosting()"); },
      dataType: 'json',
    });
    return self;
  };

  drawTopHashtag = function() {
    $("#tophashtag").html(spin);
    $.ajax({
      url: '/api/analyze/tophashtag/'+encodeURIComponent($('#keyword').text()),
      success: updateTopHashtagChart,
      error: function(){ showTryAgain("#tophashtag", "drawTopHashtag()"); },
      dataType: 'json',
    });
    return self;
  }

  drawTopURL = function() {
    $("#topurl").html(spin);
    $.ajax({
      url: '/api/analyze/topurl/'+encodeURIComponent($('#keyword').text()),
      success: updateTopURLChart,
      error: function(){ showTryAgain("#topurl", "drawTopURL()"); },
      dataType: 'json',
    });
    return self;
  }

  drawFreq().drawTopMention().drawTopPosting().drawTopHashtag().drawTopURL();

});