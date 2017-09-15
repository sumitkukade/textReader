var app = angular.module("reader", [])
app.controller("readerController", function($scope) {
    var fontSize = 20;
    $scope.fetchFileContent = function() {
    $scope.fontSize = ["10","15","20","25","30"];
    var request = {}
    $scope.count = 0;
    $scope.cnt = 0;
    request["fileName"] = $scope.name;
    request["fontSize"] = fontSize;
    request["pageCount"] = $scope.cnt;
    $.post("index.py/main",{data:JSON.stringify(request)}).done(function(response) {
      if(response == 0) {
        $scope.fileNotExists = 1;
        alert("Invalid file");
      } else {
           $scope.fileExists =  1;
           $scope.fileContent = response;
           $scope.fontObj = {
              "font-size": fontSize+"px"
           }
      }
    });
    }
    $scope.getselectval = function(size) {
         var request = {}
         request["fontSize"] = size;
         request["fileName"] = $scope.name;
         request["pageCount"] = $scope.cnt;
         alert($scope.name+size+$scope.cnt);
         $.post("index.py/fileContentWithPageNumber",{data:JSON.stringify(request)}).done(function(response) {
             alert(response);
              console.log($scope.fileContent);
         });
         $scope.fontObj = {
              "font-size": size+"px"
         }
    }
    $scope.nextPage = function() {
      var request = {}
      $scope.count++;
      if($scope.count % 2 ==0) {
        $scope.cnt = $scope.count/2;
        request["fontSize"] = fontSize;
        request["fileName"] = $scope.name;
        request["pageCount"] = $scope.cnt;
        $.post("index.py/fileContentWithPageNumber",{data:JSON.stringify(request)}).done(function(response) {
            $scope.fileContent = response;
        });
      }
    }
    $scope.backPage = function() {
      var request = {}
      $scope.count--;
      if($scope.count % 2 ==0) {
        $scope.cnt = $scope.count/2;
        request["fontSize"] = fontSize;
        request["fileName"] = $scope.name;
        request["pageCount"] = $scope.cnt;
        $.post("index.py/fileContentWithPageNumber",{data:JSON.stringify(request)}).done(function(response) {
            $scope.fileContent = response;
        });
      }
    }
});
