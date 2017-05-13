"use strict";
angular.module("foodFinderApp")
    .controller("RandomCtrl", function ($scope, $http, $location) {
        $scope.getRandomRestaurantRequest = function () {
            $http.get("/food/random/", {
                params: {
                    latitude: $scope.position.coords.latitude,
                    longitude: $scope.position.coords.longitude
                }})
                .success(function (data, status, headers, config) {
                    $scope.restaurantData = data['restaurant'];
                }).error(function (data, status, headers, config) {
                    $location.path("/404/");
                });
        };

        $scope.getRandomRestaurant = function () {
            if ($scope.position) {
                $scope.getRandomRestaurantRequest();
            } else {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position){
                        $scope.$apply(function(){
                            $scope.position = position;
                        });
                        $scope.getRandomRestaurantRequest();
                    });
                } else {
                    $location.path("/404")
                }
            }
        };

        $scope.getRandomRestaurant();

        $scope.getNewRestaurant = function () {
            $scope.restaurantData = null;
            $scope.getRandomRestaurant();
        };
    });
