var app = angular.module("reader", [])
app.controller("readerController", function($scope) {
    $scope.fetchFileContent = function() {
    var fontSize = 15;
    var request = {}
    $scope.count = 0;
    request["fileName"] = $scope.name;
    request["Size"] = fontSize;
    $.post("index.py/main",{data:JSON.stringify(request)}).done(function(response) {
      if(response == 0) {
        $scope.fileNotExists = 1;
        alert("Invalid file");
      } else {
           $scope.fileExists =  1;
           $scope.fontSize = ["10","15","20","25"];
           $scope.getselectval = function(size) {
               var request = {}
               request["fileName"] = $scope.name;
               request["Size"] = size;
             $scope.fontObj = {
                "font-size": size+"px"
              }
             $.post("index.py/main",{data:JSON.stringify(request)}).done(function(response) {
               $scope.fileContent = response;
             });

           }
           $scope.fontObj = {
              "font-size": fontSize+"px"
           }
           $scope.fileContent = response;
      }
    });
    }
    $scope.nextPage = function() {
      var request = {}
      $scope.count++;
      request["fontSize"] = 15;
      request["fileName"] = $scope.name;
      request["pageCount"] = $scope.count;
       $.post("index.py/fileContentWithPageNumber",{data:JSON.stringify(request)}).done(function(response) {
            $scope.fileContent = response;
        });

    }
});
