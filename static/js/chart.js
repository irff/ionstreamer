options_freq = {
  title: 'Growth of Tweets',
  hAxis: {title: 'Time', },
  vAxis: {title: 'Number of Tweets', },
  series: {
    // 0: {curveType: 'function'},
  },
  legend: {position: 'top', },
  animation: {startup: true, duration: 1200, easing: 'out', },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
  height: 275,
};

options_sentiment = {
  title: 'Sentiment Analytics',
  legend: {position: 'top', maxLines: 2, },
  is3D: true,
  pieSliceTextStyle: {color: 'black', },
  // pieHole: .2,
  // pieStartAngle: 180,
  colors: ['#00FF00', '#EE0000'],
  height: 275,
};

options_topmention = {
  height: 275,
  legend: {position: 'top', },
  animation: {startup: true, duration: 1200, easing: 'out', },
  title: 'Top Mentions People',
  // chartArea: {width: '100%'},
  hAxis: {
    title: 'Number of Mentions',
    minValue: 0,
  },
  vAxis: {
    title: 'Username',
  },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
};

options_topposting = {
  height: 275,
  legend: {position: 'top', },
  animation: {startup: true, duration: 1200, easing: 'out', },
  title: 'Top Posting',
  // chartArea: {width: '100%'},
  hAxis: {
    title: 'Number of Posts',
    minValue: 0,
  },
  vAxis: {
    title: 'Username',
  },
  colors: ['#4099FF', '#00FF00', '#EE0000'],
};