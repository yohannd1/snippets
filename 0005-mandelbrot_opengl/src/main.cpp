#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <GL/glut.h>

void onDisplay();
void onKeyboard(unsigned char key, int x, int y);
void onSpecial(GLint tecla, int x, int y);

int main(int argc, char** argv) {
    glutInit(&argc, argv);

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(WIN_SIZE.x, WIN_SIZE.y);

    const char* title = argv[0];
    glutCreateWindow(title);

    glClearColor(0.5f, 0.5f, 0.5f, 1.0f);

    // definir limites da janela
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);

    glutDisplayFunc(onDisplay);
    glutKeyboardFunc(onKeyboard);
    glutSpecialFunc(onSpecial);

    glutMainLoop();
    return 0;
}

void onDisplay() {
    glClear(GL_COLOR_BUFFER_BIT);
    glFlush();
}

void onKeyboard(unsigned char key, int x, int y) {
    printf("Tecla pressionada: %c (%d, 0x%x)\n", key, key, key);

    switch (key) {
    case 'q':
        exit(0);
        break;

    case ' ':
        glutPostRedisplay();
        break;
    }
}

void onSpecial(GLint tecla, int x, int y) {
    switch (tecla) { // GLUT_KEY_RIGHT GLUT_KEY_DOWN GLUT_KEY_PAGE_UP GLUT_KEY_PAGE_DOWN GLUT_KEY_F1...
    case GLUT_KEY_F12:
        glutPostRedisplay();
        break;
    case GLUT_KEY_F10:
        glutPostRedisplay();
        break;
    }
}
