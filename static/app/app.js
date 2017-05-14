"use strict";
var app = angular.module("foodFinderApp", ["ngRoute", "ui.bootstrap"]);
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

