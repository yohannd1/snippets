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

    using std::cout;
    using std::endl;

    cout << "Breadth-first search:" << endl;
    cout << ysl::bfs(g, [](int x) { return x == 20; }) << endl;

    cout << "Depth-first search:" << endl;
    cout << ysl::dfs(g, [](int x) { return x == 90; }) << endl;
}
