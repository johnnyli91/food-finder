"use strict";
angular.module("foodFinderApp")
    .controller("DetailResultsCtrl", function ($scope, $routeParams, $http, $location) {
        $scope.id = $routeParams["id"];
        $http.get("/food/result_detail/", {params: {result_id: $scope.id}})
            .success(function (data) {
                if (data['success']) {
                    $scope.resultData = data['data'];
                } else {
                    $scope.redirect404()
                }
            })
            .error(function () {
                $scope.redirect404()
            });

        $scope.updateRating = function () {
            var postData = {
                result_id: $scope.id,
                rating: $scope.resultData['rating']
            };

            $http.post("/food/result_detail/", postData)
                .success(function (data) {
                    if (data['success']) {
                        // good stuff
                    } else {
                        //bad stuff
                    }
                })
                .error(function () {
                    $scope.redirect404()
                })
        }
    });
