(function(){
  var app = angular.module("tweetlearning", ['ngSanitize']);

  app.controller('learnController', function($scope, $http, $interval){
  });

  app.filter('encodeURIComponent', function() {
    return window.encodeURIComponent;
  });

})();