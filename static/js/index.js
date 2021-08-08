$(document).ready(function() {

    $body = $("body");

    $("#index-map").click(function(event) {
        $body.addClass("loading");
        $.ajax({
            url: '/navigation/index',
            type: 'POST',
            success: function(response) {
                console.log(response);

                function connect() {

                    var ros = new ROSLIB.Ros({
                        url: 'ws://localhost:9090'
                    });



                    ros.on('connection', function() {
                        console.log('Connected to websocket server.');
                        var rosTopic = new ROSLIB.Topic({
                            ros: ros,
                            name: '/rosout',
                            messageType: 'rosgraph_msgs/Log'
                        });


                        rosTopic.subscribe(function(message) {

                            if (message.msg == "Initialization complete") {
                                console.log(message.msg)
                                window.location = "/mapping";
                                $body.removeClass("loading");
                                rosTopic.unsubscribe();
                            }

                        });

                    });


                    ros.on('close', function() {
                        console.log('Connection to websocket server closed.');

                    });


                    ros.on('error', function(error) {
                        console.log('Error connecting to websocket server: ', error);
                        setTimeout(function() {
                            connect();
                        }, 1000);

                    });
                }

                connect();



                //  setTimeout(function(){ window.location ="mapping";
                // $body.removeClass("loading"); }, 10000);

            },
            error: function(error) {
                console.log(error);
            }

        })
    });

    $("#index-list").click(function(event) {
        document.cookie = event.target.innerHTML;
        $('#exampleModal').modal('hide');


        $.ajax({

            url: '/index/navigation-precheck',
            type: 'GET',
            success: function(response) {


                if (response.mapcount > 0) {

                    $body.addClass("loading");

                    $.ajax({

                        url: '/index/gotonavigation',

                        type: 'POST',

                        data: event.target.innerHTML,

                        success: function(response) {



                            function connect() {

                                var ros = new ROSLIB.Ros({
                                    url: 'ws://localhost:9090'
                                });



                                ros.on('connection', function() {
                                    console.log('Connected to websocket server.');
                                    var rosTopic = new ROSLIB.Topic({
                                        ros: ros,
                                        name: '/rosout_agg',
                                        messageType: 'rosgraph_msgs/Log'
                                    });


                                    rosTopic.subscribe(function(message) {

                                        if (message.msg == "odom received!") {
                                            console.log(message.msg)
                                            window.location = "/navigation";
                                            $body.removeClass("loading");
                                            rosTopic.unsubscribe();
                                        }

                                    });

                                });


                                ros.on('close', function() {
                                    console.log('Connection to websocket server closed.');

                                });


                                ros.on('error', function(error) {
                                    console.log('Error connecting to websocket server: ', error);
                                    setTimeout(function() {
                                        connect();
                                    }, 1000);

                                });
                            }

                            connect();


                        },
                        error: function(error) {
                            console.log(error);
                        }

                    })


                } else {
                    alert("No map in directory.Please do mapping.")
                }
            },
            error: function(error) {
                console.log(error);
            }

        })
    });


});