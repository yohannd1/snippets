//! It seems multiple instances of `std.heap.GeneralPurposeAllocator` can be done without problems.

const std = @import("std");

test "initialize and use two allocators" {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    var gpa2 = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa2.deinit();

    const mem1 = try gpa.allocator.alloc(u8, 50);
    defer gpa.allocator.free(mem1);

    const mem2 = try gpa2.allocator.alloc(u8, 50);
    defer gpa2.allocator.free(mem2);
}
