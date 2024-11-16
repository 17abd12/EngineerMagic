$fn = 100; // Default number of sides for high resolution
ball_radius = 20; // Radius of the ball in the bearing
bearing_thickness = 5; // Thickness of the bearing casing
outer_ring_thickness = 3; // Thickness of the outer ring
inner_ring_thickness = 3; // Thickness of the inner ring
ball_diameter = 5; // Diameter of each ball
number_of_balls = 8; // Number of balls in the bearing
steel_color = [0.8, 0.8, 0.8]; // Color of steel parts
ball_color = [0.5, 0.5, 0.5]; // Color of the balls

module ball() {
    color(ball_color)
    sphere(d = ball_diameter);
}

module bearing() {
    // Outer ring
    color(steel_color)
    difference() {
        cylinder(r = ball_radius + outer_ring_thickness, h = bearing_thickness);
        translate([0, 0, -1])
            cylinder(r = ball_radius, h = bearing_thickness + 2);
    }

    // Inner ring
    translate([0, 0, -bearing_thickness / 2])
    color(steel_color)
    difference() {
        cylinder(r = ball_radius - (ball_diameter / 2 + inner_ring_thickness), h = bearing_thickness);
        translate([0, 0, -1])
            cylinder(r = ball_radius - (ball_diameter / 2 + inner_ring_thickness - inner_ring_thickness), h = bearing_thickness + 2);
    }

    // Balls
    for (i = [0 : number_of_balls - 1]) {
        rotate([0, 0, i * (360 / number_of_balls)])
        translate([ball_radius - ball_diameter / 2, 0, 0])
        ball();
    }
}

bearing();