#include <iostream>
#include <vector>
#include <set>
#include <queue>
#include <cassert>

#include "vecgraph.hh"

int main() {
    std::queue<int> q;
    q.push(5);
    q.push(10);
    assert(q.front() == 5);
    q.pop();
    assert(q.front() == 10);

    ysl::VecGraph<int> g;
    g.insert(10);
    g.insert(86);
    g.insert(90);
    g.insert(20);
    g.connect(10, 86);
    g.connect(86, 90);
    g.connect(86, 20);

    std::cout
        << ysl::bfs(g, [](int x) { return x == 20; })
        << '\n';
}
