var BASE_URL = '';

(function(){
  var app = angular.module("tweetstreamer", ['ngSanitize', 'infinite-scroll']);

  app.controller('navbarController', function($scope, $http, $interval){
    function refresh() {$http.get(BASE_URL + '/api/summary').success(function(r) {$scope.summary = r; });}
    refresh();
    $interval(refresh, 60000);
  });


  app.controller('summaryController', function($scope, $http, $interval){

    function refresh() {$http.get(BASE_URL + '/api/summary').success(function(r) {$scope.summary = r; });}

    $scope.stream = function(info, status){
      info.is_streaming = true;
      $http.post(BASE_URL + '/api/stream', {keyword: info.keyword, status: status})
      .success(refresh);
    }

    refresh();
    $interval(refresh, 5000);

    $scope.submit = function(){
      $scope.keyword = $scope.keyword.trim().toLowerCase();
      if($scope.keyword == "") return false;
      $scope.is_sending_kw = true;
      $http.post(BASE_URL + '/api/stream' , {keyword: $scope.keyword, status: 'active'})
      .success(function(){
        $http.get(BASE_URL + '/api/summary')
        .success(function(r){
          $scope.summary = r;
          $scope.is_sending_kw = false;
          $scope.keyword = '';
        })
        .error(function(){
          $scope.is_sending_kw = false;
          $scope.keyword = '';
        });
      });
    };
  });


  app.controller('analyzeController', function($scope, $http, $interval){
    $scope.keyword = $('#keyword').text();
    
    $scope.showTopRetweets = function(){
      $scope.loadtopretweets = true;
      $scope.hasretweets = false;
      $http.get(BASE_URL + '/api/analyze/topretweets/' + encodeURIComponent($scope.keyword))
      .success(function(data){
        $scope.retweets = data;
        $scope.hasretweets = true;
      });
    };

    $scope.showRandomTweets = function(){
      $scope.loadrandomtweets = true;
      $scope.hasrandomtweets = false;
      $http.get(BASE_URL + '/api/analyze/randomtweets/' + encodeURIComponent($scope.keyword))
      .success(function(data){
        $scope.randomtweets = data;
        $scope.hasrandomtweets = true;
      });
    };

    $scope.fetchTweetsAt = function(keyword, kelas, time1, time2){
      $scope.downloadlink = BASE_URL + '/download/tweetsat/' + encodeURIComponent(keyword) + '/' + kelas + '/' + encodeURIComponent(time1) + '/' + encodeURIComponent(time2) + '/tweets_at-' + keyword + '-' + (kelas == 1 ? 'positive-negative' : kelas == 2 ? 'positive' : 'negative') + '-' + (new Date(time1)).toString() + '-' + (new Date(time2)).toString() + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/gettweetsat/' + encodeURIComponent(keyword) + '/' + kelas + '/' + encodeURIComponent(time1) + '/' + encodeURIComponent(time2)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsTo = function(keyword, username){
      $scope.downloadlink = BASE_URL + '/download/mentions/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/mentions-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/getmentions/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsFrom = function(keyword, username){
      $scope.downloadlink = BASE_URL + '/download/postings/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/postings-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/getpostings/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

  });


  app.controller('learnController', function($scope, $http, $interval){
    $scope.randomtweets = [];

    $scope.loadrandomtweets = function(){
      keyword = encodeURIComponent($('#keyword').text());
      $scope.loadingrandomtweets = true;
      $http.get(BASE_URL + '/learn/randomtweets' + (keyword ? ('/' + keyword) : '') )
      .success(function(data){
        $scope.randomtweets = $scope.randomtweets.concat(data);
        $scope.loadingrandomtweets = false;
      });
    };

    $scope.learn = function(tweet, kelas){
      var oldclass = tweet.class;
      tweet.class = kelas;
      $http.post(BASE_URL + '/learn', tweet)
      .error(function(r){
        tweet.class = oldclass;
      });
    };
  });


  app.controller('classifiedController', function($scope, $http, $interval){
    $scope.tweets = [];
    $scope.allout = false;

    var size = 10, offset = 0;

    $scope.loadclassified = function(){
      $scope.loadingtweets = true;
      $http.get(BASE_URL + '/learn/classifiedtweets/'+size+'/'+offset)
      .success(function(data){
        $scope.tweets = $scope.tweets.concat(data);
        $scope.loadingtweets = false;
        offset += data.length;
        if(data.length == 0) $scope.allout = true;
      });
    };

    $scope.learn = function(tweet, kelas){
      var oldclass = tweet.class;
      tweet.class = kelas;
      $http.post(BASE_URL + '/learn', tweet)
      .error(function(r){
        tweet.class = oldclass;
      });
    };
  });

  app.filter('encodeURIComponent', function() {
    return window.encodeURIComponent;
  });

})();