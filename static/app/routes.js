"use strict";
angular.module("foodFinderApp").config(function ($routeProvider){
    $routeProvider
        .when("/", {
            templateUrl: "static/app/views/home.html",
            controller: "HomeCtrl"
        })
        .when("/random/", {
            templateUrl: "static/app/views/random.html",
            controller: "RandomCtrl"
        })
        .when("/previous_results/", {
            templateUrl: "static/app/views/previous-results.html",
            controller: "PreviousResultsCtrl"
        })
        .when("/detail_result/:id/", {
            templateUrl: "static/app/views/detail-result.html",
            controller: "DetailResultsCtrl"
        })
        .when("/404/", {
            templateUrl: "static/app/views/404.html",
            controller: ""
        })
        .otherwise({redirectTo: "/404/"});
});
