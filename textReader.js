var app = angular.module("reader", [])
app.controller("readerController", function($scope,$http) {
    $scope.Size = 20;
    $scope.fetchFileContent = function() {
    $scope.fontSize = ["10","15","20","25","30"];
    $scope.formData = {};
    $scope.cnt = 0;
    $scope.fileDetails = $scope.name+" "+$scope.cnt+" "+$scope.Size;
    $scope.formData["fileName"] = $scope.fileDetails;
    $http({
      url:"index.py/main",
      method: "POST",
      data:$.param($scope.formData),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
    .then(function(response) {
      console.log(response["data"]);
      if(response["data"] == "0"){
        $scope.fileNotExists = 1;
        $scope.Error = "Invalid File Name!!!!";
      }
      else {
         $scope.fileExists = 1;
         $scope.fileData = response["data"];
         var size = $scope.Size;
         $scope.fontObj = {
              "font-size": size+"px"
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
         $scope.formData = {};
         $scope.fileDetails = $scope.name+" "+$scope.count+" "+size;
         $scope.formData["fileName"] = $scope.fileDetails;
         $http({
                url:"index.py/main",
                method: "POST",
                data:$.param($scope.formData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
         })
         .then(function(response) {
           $scope.fileData = response["data"];
           $scope.fontObj = {
              "font-size": size+"px"
         }

         });
    }
});
