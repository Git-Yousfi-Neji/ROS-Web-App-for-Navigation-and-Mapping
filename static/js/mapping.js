var navigation = false;
var pathed = false;
var homing = false;
var MAP_WIDTH = (window.innerWidth)*0.65;
var MAP_HEIGHT = window.innerHeight - (window.innerHeight)*0.08;

$(document).ready(function() {
    $body = $("body");
    var ros = new ROSLIB.Ros({
        url: 'ws://localhost:9090'
    });

    // Create the main viewer.
    var viewer = new ROS2D.Viewer({
        divID: 'nav',
        width: MAP_WIDTH,
        height: MAP_HEIGHT
    });



    var gridClient = new NAV2D.OccupancyGridClientNav({
        ros: ros,
        rootObject: viewer.scene,
        viewer: viewer,
        serverName: '/move_base',
        continuous: true
    });

    var pan = new ROS2D.PanView({
        ros: ros,
        rootObject: viewer.scene
    });

    window.pane = function(a, b) {
        pan.startPan(a, b);
    }

    window.paned = function(c, d) {
        pan.pan(c, d);
    }

    window.zoomInMap = function(ros, viewer) {
        var zoom = new ROS2D.ZoomView({
            ros: ros,
            rootObject: viewer.scene
        });
        zoom.startZoom(250, 250);
        zoom.zoom(1.2);
    }

    window.zoomOutMap = function(ros, viewer) {
        var zoom = new ROS2D.ZoomView({
            ros: ros,
            rootObject: viewer.scene
        });
        zoom.startZoom(250, 250);
        zoom.zoom(0.8);
    }


    $("#zoomplus").click(function(event) {
        event.preventDefault();
        zoomInMap(ros, viewer);

    });

    $("#zoomminus").click(function(event) {
        event.preventDefault();
        zoomOutMap(ros, viewer);
    });

    $("#savemap").click(function(event) {
        event.preventDefault();



        var mapname = prompt("Please enter the name of the map");

        if (mapname) {
            $.ajax({
                url: '/mapping/savemap',
                type: 'POST',
                data: mapname,
                success: function(response) {
                    window.location ="/mapping";
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }

            })


        } else {
            alert("enter valid mapname to save");
        }

    });

    cmd_vel_listener = new ROSLIB.Topic({
        ros: ros,
        name: "/cmd_vel",
        messageType: 'geometry_msgs/Twist'
    });

    move = function(linear, angular) {
        var twist = new ROSLIB.Message({
            linear: {
                x: linear,
                y: 0,
                z: 0
            },
            angular: {
                x: 0,
                y: 0,
                z: angular
            }
        });
        cmd_vel_listener.publish(twist);
    }

    createJoystick = function() {
        var options = {
            zone: document.getElementById('zonejoystick'),
            threshold: 0.1,
            position: { right: '8%', bottom: '20%' },
            mode: 'static',
            size: 150,
            color: 'blue',
        };
        manager = nipplejs.create(options);

        linear_speed = 0;
        angular_speed = 0;

        manager.on('start', function(event, nipple) {
            timer = setInterval(function() {
                move(linear_speed, angular_speed);
            }, 25);
        });

        manager.on('move', function(event, nipple) {
            max_linear = 0.2; // m/s
            max_angular = 0.8; // rad/s
            max_distance = 75.0; // pixels;
            linear_speed = Math.sin(nipple.angle.radian) * max_linear * nipple.distance / max_distance;
            angular_speed = -Math.cos(nipple.angle.radian) * max_angular * nipple.distance / max_distance;
        });

        manager.on('end', function() {
            if (timer) {
                clearInterval(timer);
            }
            self.move(0, 0);
        });
    }


    window.onload = function() {
        createJoystick();
    }

    $('.menu-btn').click(function() {
        $(this).toggleClass("menu-btn-left");
        $('.box-out').toggleClass('box-in');
    });


    $("#start-nav-button").click(function() {
        event.preventDefault();
    });

    $("#index-list-map").click(function(event) {

        document.cookie =  event.target.innerHTML  ;    
        $('#exampleModal').modal('hide');
        $.ajax({
            url: '/mapping/cutmapping',
            type: 'POST',
            success: function(response) {

                $.ajax({
                    url: '/index/navigation-precheck',
                    type: 'GET',
                    success: function(response) {
                        console.log(response.mapcount);
                        if (response.mapcount > 0) {
                            $body.addClass("loading");
                            $.ajax({
                                url: '/index/gotonavigation',
                                type: 'POST',
                                data: event.target.innerHTML,
                                success: function(response) {

                                    // console.log(response)


                                    var rosTopic = new ROSLIB.Topic({
                                        ros: ros,
                                        name: '/rosout_agg',
                                        messageType: 'rosgraph_msgs/Log'
                                    });

                                    rosTopic.subscribe(function(message) {

                                        // console.log(message.msg)                    
                                        if (message.msg == "odom received!") {
                                            console.log(message.msg)
                                            window.location = "/navigation";
                                            $body.removeClass("loading");
                                            // window.location = "/navigation";
                                        }

                                    });

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

            },
            error: function(error) {
                console.log(error);
            }

        })

    });




});