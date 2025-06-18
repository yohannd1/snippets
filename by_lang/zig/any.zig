const std = @import("std");

// An attempt at implementing what... I think C++'s std::any is?
//
// Projected for zig 0.14.0

const Any = struct {
    ptr: *OpaqueType,
    type_hash: u64,

    const Self = @This();
    pub const OpaqueType = opaque {};

    pub fn hashType(comptime T: type) u64 {
        // FIXME: this implementation probably falls apart the moment there is a hash collision. What I need is unique
        // identifiers.
        return std.hash_map.hashString(@typeName(T));
    }

    pub fn init(ptr: anytype) Self {
        const T = @TypeOf(ptr);

        const Inner = switch (@typeInfo(T)) {
            .pointer => |p| p.child,
            else => |_| @compileError("expected pointer, found " ++ @typeName(T)),
        };

        return .{
            .ptr = if (@sizeOf(Inner) == 0) undefined else @ptrCast(ptr),
            .type_hash = hashType(Inner),
        };
    }

    pub fn guess(self: *Self, comptime T: type) ?*T {
        if (self.type_hash == hashType(T))
            return @ptrCast(@alignCast(self.ptr));
        return null;
    }
};

pub fn main() void {
    var num: i64 = 25; // try changing this into another type and see the magic happening
    var a = Any.init(&num);

    if (a.guess(i64)) |i| {
        std.debug.print("i64! {}\n", .{i.*});
    }

    if (a.guess(i32)) |i| {
        std.debug.print("i32! {}\n", .{i.*});
    }
}
