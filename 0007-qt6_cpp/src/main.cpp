#include <QApplication>
#include <QDebug>
#include <QPushButton>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    auto btn = QPushButton("omg hii");
    btn.connect(&btn, &QPushButton::clicked, &btn, [&]() {
        qDebug() << "OK";
    });
    btn.show();

    return app.exec();
}
