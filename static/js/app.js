(function(){
  var app = angular.module("tweetstreamer", ['ngSanitize']);

  app.controller('summaryController', function($scope, $http, $interval){

    function refresh() {$http.get('/api/summary').success(function(r) {$scope.summary = r; }); }

    $scope.stream = function(info, status){
      info.is_streaming = true;
      $http.post('/api/stream', {keyword: info.keyword, status: status})
      .success(refresh);
    }

    refresh();
    $interval(refresh, 4000);

    $scope.submit = function(){
      $scope.keyword = $scope.keyword.trim().toLowerCase();
      if($scope.keyword == "") return false;
      $scope.is_sending_kw = true;
      $http.post(
        '/api/stream' ,
        {keyword: $scope.keyword, status: 'active'}
      ).success(function(){
        $scope.is_sending_kw = false;
        refresh();
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

    $scope.fetchTweetsAt = function(keyword, time1, time2){
      $scope.hastweets = false;
      $http.get('/api/analyze/gettweetsat/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(time1) + '/' + encodeURIComponent(time2)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsTo = function(keyword, username){
      $scope.hastweets = false;
      $http.get('/api/analyze/getmentions/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

    $scope.fetchTweetsFrom = function(keyword, username){
      $scope.hastweets = false;
      $http.get('/api/analyze/getpostings/' + encodeURIComponent(keyword) + '/' + encodeURIComponent(username)).success(function(r){
        $scope.tweets = r;
        $scope.hastweets = true;
      });
    };

  });


  app.filter('encodeURIComponent', function() {
    return window.encodeURIComponent;
  });

/*  app.animation('.slide', [function() {
    return {
      // make note that other events (like addClass/removeClass)
      // have different function input parameters
      enter: function(element, doneFn) {
        jQuery(element).fadeIn(400, doneFn);

        // remember to call doneFn so that angular
        // knows that the animation has concluded
      },

      move: function(element, doneFn) {
        jQuery(element).fadeIn(400, doneFn);
      },

      leave: function(element, doneFn) {
        jQuery(element).fadeOut(400, doneFn);
      }
    }
  }]);*/

})();

/*  .controller('titleController', function(){
    this.title = 'SAPI';
  });*/

/*function addone(id, data) {
  cl = $('#sample').clone();
  cl.attr('id', id);
  if (data['status'] == 'processing') cl.addClass('animated jello');
  if (data['status'] == 'inactive') cl.find('.title').css('background', 'grey');
  cl.show();
  childs = cl.children().children();
  childs[0].innerHTML = data['name'];
  childs[1].innerHTML = data['counts'];
  childs[2].innerHTML = data['status'];
  childs[3].innerHTML = data['tw1'];
  childs[4].innerHTML = data['tw2'];
  childs[5].innerHTML = data['tw3'];
  if(data['status'] == 'active')
    childs[6].innerHTML = '<span onclick="stream(this,\'inactive\');"><a class="button radius secondary tiny"><i class="fa fa-pause"></i></a></span> <span onclick="unstream(this);"><a class="button radius alert tiny"><i class="fa fa-trash"></i></a></span>';
  if(data['status'] == 'inactive')
    childs[6].innerHTML = '<span onclick="stream(this,\'active\');"><a class="button radius success tiny"><i class="fa fa-play"></i></a></span> <span onclick="unstream(this);"><a class="button radius alert tiny"><i class="fa fa-trash"></i></a></span>';
  panel.append(cl);
}

function refresh() {
  $.get('/api/summary', function (response) {
    panel.empty();
    for (var i = 0; i < response.length; ++i) {
      addone('id-'+i, response[i]);
    };
  }, "json");
}

function addkeyword() {
  $('#plus_button').prop({disabled:true});
  $('#content_button').attr('class', 'fa fa-lg fa-spinner fa-spin');
  keyword = $('#keyword').val().trim()+'@'+$('#username').val().trim()
  if(keyword == '@') return false
  $.post('/stream', {keyword: keyword, status: 'active', datestamp: (new Date()).toISOString().slice(0,10)}, function(response){
    $('#plus_button').prop({disabled:false});
    $('#content_button').attr('class', 'fa fa-lg fa-plus');
    $('#message').text('@'+$('#username').val().trim()+' - '+$('#keyword').val().trim()+' has been added to queue successfully');
    $('#username').val('');
    $('#keyword').val('');
    refresh();
  }, "json");
  return false;
}

function stream(node, status) {
  // $.ajax({type:'DELE', url:'/api/stream', success: function(r){console.log(r)}})
  $.post('/api/stream', {keyword: node.parentNode.parentNode.children[0].innerHTML, status: status}, function(response){
    // console.log(response);
    refresh();
  }, "json");
}

function unstream(node) {
  $.post('/unstream', {keyword: node.parentNode.parentNode.children[0].innerHTML}, function(response){
    // console.log(response);
    refresh();
  }, "json");
}

$(function(){
  panel = $('#panel');
  function loop_refresh() {
    refresh();
    setTimeout(loop_refresh, 3000);
  }
  loop_refresh();
});*/
