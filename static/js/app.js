(function(){
  var app = angular.module("tweetstreamer", ['ngSanitize', 'infinite-scroll']);

  app.controller('navbarController', function($scope, $http, $interval){
    function refresh() {$http.get('/api/summary').success(function(r) {$scope.summary = r; });}
    refresh();
    $interval(refresh, 3500);
  });


  app.controller('summaryController', function($scope, $http, $interval){

    function refresh() {$http.get('/api/summary').success(function(r) {$scope.summary = r; });}

    $scope.stream = function(info, status){
      info.is_streaming = true;
      $http.post('/api/stream', {keyword: info.keyword, status: status})
      .success(refresh);
    }

    refresh();
    $interval(refresh, 3500);

    $scope.submit = function(){
      $scope.keyword = $scope.keyword.trim().toLowerCase();
      if($scope.keyword == "") return false;
      $scope.is_sending_kw = true;
      $http.post(
        '/api/stream' ,
        {keyword: $scope.keyword, status: 'active'}
      ).success(function(){
        $http.get('/api/summary').success(function(r) {
          $scope.summary = r;
          $scope.is_sending_kw = false;
        });
      });
      $scope.keyword = '';
    };
  });


  app.controller('analyzeController', function($scope, $http, $interval){
    $scope.showTopRetweets = function(){
      $scope.loadtopretweets = true;
      $scope.hasretweets = false;
      $http.get('/api/analyze/topretweets/' + encodeURIComponent($('#keyword').text()))
      .success(function(data){
        $scope.retweets = data;
        $scope.hasretweets = true;
      });
    };

    $scope.showRandomTweets = function(){
      $scope.loadrandomtweets = true;
      $scope.hasrandomtweets = false;
      $http.get('/api/analyze/randomtweets/' + encodeURIComponent($('#keyword').text()))
      .success(function(data){
        $scope.randomtweets = data;
        $scope.hasrandomtweets = true;
      });
    };

    $scope.fetchTweetsAt = function(keyword, kelas, time1, time2){
      $scope.modaltitle = kelas == 1 ? 'All' : kelas == 2 ? 'Positive' : 'Negative' + ' tweets of '+keyword;
      $scope.downloadlink = '/download/tweetsat/' + encodeURIComponent(keyword) + '/' + kelas + '/' + encodeURIComponent(time1) + '/' + encodeURIComponent(time2) + '/tweets_at-' + keyword + '-' + (kelas == 1 ? 'all' : kelas == 2 ? 'positive' : 'negative') + '-' + (new Date(time1)).toString() + '-' + (new Date(time2)).toString() + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get('/api/analyze/gettweetsat/' + encodeURIComponent(keyword) + '/' + kelas + '/' + encodeURIComponent(time1) + '/' + encodeURIComponent(time2)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsTo = function(keyword, username){
      $scope.modaltitle = 'Tweets about ' + keyword + ' that Mentions to ' + username;
      $scope.downloadlink = '/download/mentions/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/mentions-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get('/api/analyze/getmentions/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsFrom = function(keyword, username){
      $scope.modaltitle = 'Tweets about ' + keyword + ' from ' + username;
      $scope.downloadlink = '/download/postings/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/postings-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get('/api/analyze/getpostings/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

  });


  app.controller('learnController', function($scope, $http, $interval){
    $scope.randomtweets = [];

    $scope.loadrandomtweets = function(){
      $scope.loadingrandomtweets = true;
      $http.get('/learn/randomtweets')
      .success(function(data){
        $scope.randomtweets = $scope.randomtweets.concat(data);
        $scope.loadingrandomtweets = false;
      });
    };

    $scope.learn = function(tweet, kelas){
      tweet.class = kelas;
      $http.post('/learn', tweet)
      .error(function(r){
        tweet.class = '';
      });
    };
  });


  app.controller('classifiedController', function($scope, $http, $interval){
    $scope.tweets = [];
    $scope.allout = false;

    var size = 10, offset = 0;

    $scope.loadclassified = function(){
      $scope.loadingtweets = true;
      $http.get('/learn/classifiedtweets/'+size+'/'+offset)
      .success(function(data){
        $scope.tweets = $scope.tweets.concat(data);
        $scope.loadingtweets = false;
        offset += data.length;
        if(data.length == 0) $scope.allout = true;
      });
    };

    $scope.learn = function(tweet, kelas){
      tweet.class = kelas;
      $http.post('/learn', tweet)
      .success(function(r){
        // console.log(r);
      });
    };
  });

  app.filter('encodeURIComponent', function() {
    return window.encodeURIComponent;
  });

})();