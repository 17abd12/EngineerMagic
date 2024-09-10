sides = 100;
ball_radius = 2;
n_balls = 8;
ball_color = [0.8, 0.4, 0];
inner_ring_radius = 8;
outer_ring_radius = 12;
inner_ring_width = 2;
outer_ring_width = 2;
inner_color = [0.3, 0.3, 0.3];
outer_color = [0.5, 0.5, 0.5];

// Ball bearing assembly
module bearing() {
    outer_ring();
    inner_ring();
    balls();
}

module outer_ring() {
    difference() {
        color(outer_color)
        cylinder(h = outer_ring_width, r = outer_ring_radius, $fn = sides);
        translate([0, 0, -1])
        cylinder(h = outer_ring_width + 2, r = inner_ring_radius + ball_radius, $fn = sides);
    }
}

module inner_ring() {
    color(inner_color)
    translate([0, 0, (outer_ring_width - inner_ring_width) / 2])
    cylinder(h = inner_ring_width, r = inner_ring_radius, $fn = sides);
}

module balls() {
    for (i = [0 : 360/n_balls : 359]) {
        rotate([0, 0, i])
        translate([inner_ring_radius + ball_radius, 0, (outer_ring_width - ball_radius * 2) / 2])
        color(ball_color)
        sphere(r = ball_radius, $fn = sides);
    }
}

bearing();