"use strict";
angular.module("foodFinderApp")
    .controller("PreviousResultsCtrl", function ($scope, $http, $location) {
        $http.get("/food/previous_result/")
            .success(function (data) {
                $scope.previousResults = data['data'];
                $scope.hasResults = data['has_results'];
            }).error(function () {
                $location.path("/404/");
            })
    });
