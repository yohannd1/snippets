#ifndef _DEFER_HH
#define _DEFER_HH

/**
 * Runs a function after its scope is exited. Inspired by Zig's "defer" keyword.
 *
 * Inspired by https://www.gingerbill.org/article/2015/08/19/defer-in-cpp/
 */
template <typename F>
struct _Deferred {
    F m_func;
    _Deferred(F func): m_func(func) {}
    ~_Deferred() { m_func(); }
};

template <typename F>
_Deferred<F> make_defer(F func) {
    return _Deferred<F>(func);
}

#define _DEFER_CONCAT(_a, _b) _a ## _b
#define _DEFER_CONCAT2(_a, _b) _DEFER_CONCAT(_a, _b)
#define _DEFER_GENSYM() _DEFER_CONCAT2(_deferred_, __LINE__)

#define DEFER(_expr) const auto _DEFER_GENSYM() = make_defer([&]() _expr);

#endif
