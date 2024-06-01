#ifndef _YSL_VECGRAPH_HH
#define _YSL_VECGRAPH_HH

namespace ysl {

template <typename T>
struct VecGraph {
    std::vector<T> vertexes;
    std::vector<std::pair<T, T>> edges;

    void insert(T vertex) {
        vertexes.push_back(vertex);
    }

    void connect(T v1, T v2) {
        edges.push_back({v1, v2});
    }
};

template <typename T, typename C>
static bool contains(const C& c, T t) {
    return c.find(t) != c.end();
}

/**
 * Find a vertex v in g that satisfies f(g), via breadth-first search.
 */
template <typename T, typename F>
static bool bfs(const VecGraph<T>& g, F f) {
    if (g.vertexes.size() == 0)
        return false;

    std::set<T> visited;
    std::queue<T> next;
    next.push(g.vertexes.at(0));

    while (next.size() > 0) {
        T v = next.front();

        std::cout << "Visiting " << v << '\n';

        if (f(v))
            return true;
        next.pop(); // is this the right one?
        visited.insert(v);

        for (auto e : g.edges) {
            if (e.first == v && !contains(visited, e.second)) {
                next.push(e.second);
            }
        }
    }

    return false;
}

/**
 * Find a vertex v in g that satisfies f(g), via depth-first search.
 */
template <typename T, typename F>
static bool dfs(const VecGraph<T>& g, F f) {
    if (g.vertexes.size() == 0)
        return false;

    std::set<T> visited;
    std::vector<T> next;
    next.push_back(g.vertexes.at(0));

    while (next.size() > 0) {
        T v = next.back();

        std::cout << "Visiting " << v << '\n';

        if (f(v))
            return true;
        next.pop_back(); // is this the right one?
        visited.insert(v);

        for (auto e : g.edges) {
            if (e.first == v && !contains(visited, e.second)) {
                next.push_back(e.second);
            }
        }
    }

    return false;
}

}

#endif
