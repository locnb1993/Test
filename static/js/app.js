/// <reference path="angular.js" />
var myApp = angular.module('myApplication', []);

// Create the factory that share the Fact
myApp.factory('Mode', function () {
    var data = { UserMode: '' };

    return {
        getUserMode: function () {
            return data.UserMode;
        },
        setUserMode: function (UserMode) {
            data.UserMode = UserMode;
        }
    };
});

myApp.config(function ($routerProvider) {
    $routerProvider
    .when('/', {
        templateURL: '/Welcome.html',
        controller: 'loginController'
    })
    .when('/home', {
        templateURL: '/Home.html',
        controller: 'HomeCtrl'
    })
    .otherwise({
        template: '404'
    })
})

myApp.controller('loginController', ['$scope', '$window', 'Mode', function ($scope, $window, Mode) {
    $scope.userInfo = {};

    $scpoe.user = {};

    $scope.login = function () {
        $http({
            method: 'POST',
            url: '/login',
            data: { userInfo: $scope.userInfo }
        }).then(function (response) {
            console.log(response);
            if (response.data.auth != '1')
            {
                $window.alert('Wrong username or password. Please try again!')
            }
            else
            {
                Mode.setUserMode($scope.userInfo.username)
            }
        }, function (error) {
            console.log(error);
        });
    }
}])

myApp.controller('HomeController', function ($scope, $http, Mode) {
    $scope.adminMode = function(){
		if (Mode.getUserMode == 'admin')
			return true;
		else
			return false;
	};

    $scope.AccountInfo = {};

    $scope.showAdd = true;

    $scope.showlist = function () {
        $http({
            method: 'POST',
            url: '/getAccountList',

        }).then(function (response) {
            $scope.Accounts = response.data;
            console.log('mm', $scope.Accounts);
        }, function (error) {
            console.log(error);
        });
    }

    $scope.addAccount = function () {

        $http({
            method: 'POST',
            url: '/addAccount',
            data: { AccountInfo: $scope.AccountInfo }
        }).then(function (response) {
            $scope.showlist();
            $('#addPopUp').modal('hide')
            $scope.AccountInfo = {}
        }, function (error) {
            console.log(error);
        });
    }

    $scope.editAccount = function (id) {
        $scope.AccountInfo.id = id;

        $scope.showAdd = false;

        $http({
            method: 'POST',
            url: '/getAccount',
            data: { id: $scope.AccountInfo.id }
        }).then(function (response) {
            console.log(response);
            $scope.AccountInfo = response.data;
            $('#addPopUp').modal('show')
        }, function (error) {
            console.log(error);
        });
    }

    $scope.updateAccount = function (id) {

        $http({
            method: 'POST',
            url: '/updateAccount',
            data: { AccountInfo: $scope.AccountInfo }
        }).then(function (response) {
            console.log(response.data);
            $scope.showlist();
            $('#addPopUp').modal('hide')
        }, function (error) {
            console.log(error);
        });
    }

    $scope.showAddPopUp = function () {
        $scope.showAdd = true;
        $scope.AccountInfo = {};
        $('#addPopUp').modal('show')
    }

    $scope.confirmDelete = function (id) {
        $scope.deleteAccountId = id;
        $('#deleteConfirm').modal('show');
    }

    $scope.deleteAccount = function () {
        $http({
            method: 'POST',
            url: '/deleteAccount',
            data: { id: $scope.deleteAccountId }
        }).then(function (response) {
            console.log(response.data);
            $scope.deleteAccountId = '';
            $scope.showlist();
            $('#deleteConfirm').modal('hide')
        }, function (error) {
            console.log(error);
        });
    }

})