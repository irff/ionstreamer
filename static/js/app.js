var BASE_URL = '';

(function(){
  var app = angular.module("tweetstreamer", ['ngSanitize', 'infinite-scroll']);

  app.controller('navbarController', function($scope, $http, $interval){
    $scope.summary = [];
    var refresh = function() {
      $http.get(BASE_URL + '/api/summary').success(function(r) {
        var current_keywords = $scope.summary.map(function(info){return info.keyword});
        var next_keywords = r.map(function(info){return info.keyword});
        if(current_keywords.join('|') == next_keywords.join('|'))
        {
          for (var i = 0; i < r.length; ++i) {
            $scope.summary[i].count = r[i].count;
            $scope.summary[i].status = r[i].status;
          }
        } else $scope.summary = r;
      });
    };
    refresh();
    $interval(refresh, 60000);
  });


  app.controller('streamingController', function($scope, $http, $interval){

    $scope.summary = [];
    var block_refresh = false;

    var refresh = function() {
      if(block_refresh) return;
      block_refresh = true;
      $http.get(BASE_URL + '/api/summary')
      .success(function (r) {
        $scope.summary.splice(r.length);
        var i = 0;
        var changeSummary = function(){
          if(i < r.length) {
            var to = 0;
            if(i == $scope.summary.length) $scope.summary.push({});
            if($scope.summary[i].keyword == r[i].keyword && $scope.summary[i].status == r[i].status) {
              $scope.summary[i].count = r[i].count;
              $scope.summary[i].processing = r[i].processing;
              $scope.summary[i].tweets = r[i].tweets;
            } else{
              $scope.summary[i] = r[i];
              $scope.$applyAsync();
              to = 400;
            }
            ++i;
            setTimeout(changeSummary, to);
          } else block_refresh = false;
        };
        changeSummary();
      });
    };

    $scope.stream = function(info, status){
      info.is_streaming = true;
      if(status == "active") info.playing = true; else
      if(status == "inactive") info.pausing = true; else
      if(status == "removed") info.removing = true;
      block_refresh = true;
      setTimeout(function(){block_refresh = false;}, status == "removed" ? 2100 : 1400);
      $http.post(BASE_URL + '/api/stream', {keyword: info.keyword, status: status})
      .success(function(){
        var tryRefresh = function(){
          if(block_refresh) setTimeout(tryRefresh, 100);
          else refresh();
        };
        tryRefresh();
      })
      .error(function(){
        info.is_streaming = false;
        var tryFail = function(){
          if(block_refresh) setTimeout(tryFail, 100);
          else {
            info.failed = true;
            if(status == "active") info.playing = false; else
            if(status == "inactive") info.pausing = false; else
            if(status == "removed") info.removing = false;
          }
        };
        tryFail();
      });
    };

    refresh();
    $interval(refresh, 500);

    $scope.submit = function(){
      kword = $scope.keyword.trim().toLowerCase();
      if(kword == "") return false;
      $scope.is_sending_kw = true;
      $http.post(BASE_URL + '/api/stream' , {keyword: kword, status: 'active', last_modified: '0000-00-00 00:00:00'})
      .success(function(){
        $http.get(BASE_URL + '/api/summary')
        .success(function(r){
          $scope.is_sending_kw = false;
          $scope.keyword = '';
          refresh();
        })
        .error(function(){
          $scope.is_sending_kw = false;
          refresh();
        });
      });
    };
  });


  app.controller('analyzeController', function($scope, $http, $interval){
    $scope.keyword = $('#keyword').text();

    $interval(function(){$http.get(BASE_URL + '/api/total/'+$scope.keyword).success(function(r) {$scope.total = r;});}, 5000);

    $scope.showTopRetweets = function(){
      $scope.loadtopretweets = true;
      $scope.hasretweets = false;
      $http.get(BASE_URL + '/api/analyze/topretweets/' + encodeURIComponent($scope.keyword))
      .success(function(data){
        $scope.retweets = data;
        $scope.hasretweets = true;
      })
      .error(function(){
        $scope.loadtopretweets = false;
      });
    };

    $scope.showRandomTweets = function(){
      $scope.loadrandomtweets = true;
      $scope.hasrandomtweets = false;
      $http.get(BASE_URL + '/api/analyze/randomtweets/' + encodeURIComponent($scope.keyword))
      .success(function(data){
        $scope.randomtweets = data;
        $scope.hasrandomtweets = true;
      })
      .error(function(){
        $scope.loadtopretweets = false;
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
      $scope.downloadlink = BASE_URL + '/download/mention/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/mention-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/getmention/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsFrom = function(keyword, username){
      $scope.downloadlink = BASE_URL + '/download/posting/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username) + '/posting-' + keyword + '-' + username + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/getposting/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsHashtag = function(keyword, hashtag){
      $scope.downloadlink = BASE_URL + '/download/hashtag/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(hashtag) + '/posting-' + keyword + '-' + hashtag + '.csv';
      $scope.tweets = [];
      $scope.hastweets = false;
      $http.get(BASE_URL + '/api/analyze/gethashtag/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(hashtag)).success(function(r){
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