var CheckApp = angular.module('CheckApp', []);

var socket = io.connect('https://' + document.domain + ':' + location.port + '/check');

CheckApp.controller('CheckController', function($scope){
    
    $scope.name = '';
    $scope.text = '';
    $scope.searchResults = [];
    // $scope.searchID = '';
    
    $scope.search = function search(){
        console.log('Search result: ', $scope.text);
        socket.emit('search', $scope.text);
        $scope.text = '';
    };
    
    $scope.searchApproval = function searchApproval(){
        console.log('approval results: ', $scope.text);
        socket.emit('searchApproval', $scope.text);
        $scope.text = '';
    };
    
    $scope.approval = function approval(){
        console.log('approval results: ', $scope.searchID);
        socket.emit('approval', $scope.searchID);
    };
    
    socket.on('searchResults', function(results){
        if (results.length > 0) {
            $("#searchResultsPanel").show();
        }
        else {
            $("#searchResultsPanel").hide();
        }
        for(var i = 0; i < results.length; i++){
            console.log(results[i]);
            $scope.searchResults.push(results[i]);
        }
        $scope.$apply();
        $scope.searchResults = [];
    });
    
    socket.on('approvalResults', function(results){
        if (results.length > 0) {
            $("#searchResultsPanel").show();
        }
        else {
            $("#searchResultsPanel").hide();
        }
        for(var i = 0; i < results.length; i++){
            console.log(results[i]);
            $scope.searchResults.push(results[i]);
        }
        $scope.$apply();
        $scope.searchResults = [];
    });
});