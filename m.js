var app = angular.module('sampleapp', [])
app.controller('samplecontrol', function ($scope) {
     $scope.sample = ["10","20"];
     var num;
     $scope.getselectval = function () {
        num = $scope.selitem;
    }
   alert(num);
})
