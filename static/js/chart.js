options_freq = {
  title: 'Growth of Tweets',
  hAxis: {title: 'Time', },
  vAxis: {title: 'Number of Tweets', },
  series: {
    // 0: {curveType: 'function'},
  },
  legend: {position: 'top', },
  animation: {startup: true, duration: 1000, easing: 'out', },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
  height: 300,
};

options_sentiment = {
  title: 'Sentiment Analytics',
  legend: {position: 'top', maxLines: 2, },
  is3D: true,
  pieSliceTextStyle: {color: 'black', fontSize: 12, },
  // pieHole: .2,
  // pieStartAngle: 180,
  colors: ['#00FF00', '#EE0000'],
  height: 300,
};

options_topmention = {
  height: 300,
  legend: {position: 'top', },
  animation: {startup: true, duration: 1000, easing: 'out', },
  title: 'Top Mentions People',
  // chartArea: {width: '50%'},
  hAxis: {
    title: 'Number of Mentions',
    minValue: 0,
    textStyle: {
      bold: true,
      fontSize: 12,
      color: '#4d4d4d'
    },
    titleTextStyle: {
      bold: true,
      fontSize: 18,
      color: '#4d4d4d'
    }
  },
  vAxis: {
    title: 'Username',
    textStyle: {
      fontSize: 14,
      bold: true,
      color: '#848484'
    },
    titleTextStyle: {
      fontSize: 14,
      bold: true,
      color: '#848484'
    }
  },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
};

options_topposting = {
  height: 300,
  legend: {position: 'top', },
  animation: {startup: true, duration: 1000, easing: 'out', },
  title: 'Top Posting',
  // chartArea: {width: '50%'},
  hAxis: {
    title: 'Number of Posts',
    minValue: 0,
    textStyle: {
      bold: true,
      fontSize: 12,
      color: '#4d4d4d'
    },
    titleTextStyle: {
      bold: true,
      fontSize: 18,
      color: '#4d4d4d'
    }
  },
  vAxis: {
    title: 'Username',
    textStyle: {
      fontSize: 14,
      bold: true,
      color: '#848484'
    },
    titleTextStyle: {
      fontSize: 14,
      bold: true,
      color: '#848484'
    }
  },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
};