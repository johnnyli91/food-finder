"use strict";
angular.module("foodFinderApp")
    .controller("HomeCtrl", function ($scope, $http, $location) {
        $scope.getRandomRestaurant = function () {
            $location.path("/random/");
        };
    });
