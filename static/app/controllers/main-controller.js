"use strict";
angular.module("foodFinderApp")
    .controller("MainCtrl", function ($scope, $http, $location) {
        $scope.redirect404 = function () {
            $location.path("/404/")
        };

        $scope.ratingTitles = ['Awful', 'Bad', 'Alright', 'Good', 'Amazing']
    });
