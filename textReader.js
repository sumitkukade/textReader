var app = angular.module("reader", [])
app.controller("readerController", function($scope) {
    var fontSize = 20;
    $scope.fetchFileContent = function() {
    $scope.fontSize = ["10","15","20","25","30"];
    var request = {}
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
            $scope.fileData = JSON.parse(response)
           $scope.fontObj = {
              "font-size": fontSize+"px"
           }
      }
    });
    $scope.nextPage = function() {
      if($scope.count < ($scope.fileData["sizeOfFile"])) {
         $scope.count++;
      }
      else {
        $scope.count = 0;
      }
    }

    $scope.backPage = function() {
     if($scope.count > 0 ) {
      $scope.count--;
     }
      else {
        $scope.count = $scope.fileData["sizeOfFile"];
      }
    }
 }
    $scope.getselectval = function(size) {
         var request = {}
         request["fontSize"] = size;
         request["fileName"] = $scope.name;
         request["pageCount"] = $scope.cnt;
         alert($scope.name+size+$scope.cnt);
         $.post("index.py/main",{data:JSON.stringify(request)}).done(function(response) {
             alert(response);
              console.log($scope.fileContent);
         });
         $scope.fontObj = {
              "font-size": size+"px"
         }
    }

});
