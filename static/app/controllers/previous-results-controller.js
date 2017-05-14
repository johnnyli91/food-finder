"use strict";
angular.module("foodFinderApp")
    .controller("PreviousResultsCtrl", function ($scope, $http, $location) {
        $http.get("/food/previous_result/")
            .success(function (data) {
                $scope.previousResults = data;
            }).error(function () {
                $location.path("/404/");
            })
    });
