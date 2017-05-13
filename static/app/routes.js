"use strict";
angular.module("foodFinderApp").config(function ($routeProvider){
    $routeProvider
        .when("/", {
            templateUrl: "static/app/views/home.html",
            controller: "HomeCtrl"
        })
        .when("/random", {
            templateUrl: "static/app/views/random.html",
            controller: "RandomCtrl"
        })
        .when("/404", {
            templateUrl: "static/app/views/404.html",
            controller: ""
        })
        .otherwise({redirectTo: "/404"});
});
