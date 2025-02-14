// A simple CRTP/mixin example. Not sure what to use it for though.
//
// Target version: 0.14.0-dev.3220+cb5547e3d

const std = @import("std");

pub fn CrtpMixin(comptime T: type) type {
    return struct {
        pub fn thing(self: T) i32 {
            return self.x + self.y;
        }
    };
}

pub const SomeStruct = struct {
    x: i32,
    y: i32,

    pub usingnamespace CrtpMixin(@This());
};

pub fn main() anyerror!void {
    const s = SomeStruct{ .x = 10, .y = 20 };
    std.debug.print("{}\n", .{s.thing()});
}
