sides = 100;
outer_radius = 50;
inner_radius = 20;
bearing_width = 15;
ball_radius = 5;
num_balls = 12;
ball_color = [1, 0, 0];
ring_color = [0.4, 0.4, 0.4];

module ball_bearing() {
    // Outer Ring
    color(ring_color)
    difference() {
        cylinder(h = bearing_width, r = outer_radius, $fn = sides);
        cylinder(h = bearing_width, r = outer_radius - 5, $fn = sides);
    }

    // Inner Ring
    color(ring_color)
    difference() {
        cylinder(h = bearing_width, r = inner_radius, $fn = sides);
        cylinder(h = bearing_width, r = inner_radius - 5, $fn = sides);
    }

    // Balls
    for (i = [0 : 360/num_balls : 360 - 360/num_balls]) {
        x = (outer_radius + inner_radius) / 2 * cos(i);
        y = (outer_radius + inner_radius) / 2 * sin(i);
        translate([x, y, bearing_width / 2])
        color(ball_color)
        sphere(r = ball_radius, $fn = sides);
    }
}

// Assemble the ball bearing
ball_bearing();