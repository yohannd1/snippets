#include <SDL2/SDL.h>
#include <stdio.h>
#include <math.h>

#define WIDTH 600
#define HEIGHT 600

#define REAL_SET_START -2
#define REAL_SET_END 1
#define IMAGINARY_SET_START -1
#define IMAGINARY_SET_END 1
#define MAX_ITERATION 120

#define TRUE 1
#define FALSE 0

typedef struct State {
	double scale;
	double camera_x;
	double camera_y;
	double move_amount;
} State;

typedef struct MandelbrotResult {
	int is_in;
	int iteration_count;
} MandelbrotResult;

void draw(SDL_Renderer* r, const State const* st);
void draw_loading_identifier(SDL_Renderer* r);
void die(const char* c);
MandelbrotResult mandelbrot(double c_x, double c_y);

int main(int argc, char *argv[])
{
	SDL_Init(SDL_INIT_VIDEO);

	SDL_Window *window = SDL_CreateWindow("Hello, World! :D",
			SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
			WIDTH, HEIGHT,
			0);

	SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (renderer == NULL) {
		die("Failed to create renderer");
	}

	State st = {
		.scale = WIDTH,
		.camera_x = 0.0,
		.camera_y = 0.0,
		.move_amount = 0.05,
	};

	int has_updated = TRUE;
	int running = TRUE;
	while (running) {

		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			switch (event.type) {
			case SDL_QUIT:
				running = FALSE;
				break;
			case SDL_KEYDOWN:
				int keycode = event.key.keysym.sym;
				switch (keycode) {
				case SDLK_q:
					running = FALSE;
					break;
				case SDLK_RIGHT:
					st.camera_x += st.move_amount;
					has_updated = TRUE;
					break;
				case SDLK_LEFT:
					st.camera_x -= st.move_amount;
					has_updated = TRUE;
					break;
				case SDLK_DOWN:
					st.camera_y += st.move_amount;
					has_updated = TRUE;
					break;
				case SDLK_UP:
					st.camera_y -= st.move_amount;
					has_updated = TRUE;
					break;
				case SDLK_j:
					st.scale *= 1.5;
					st.move_amount -= st.move_amount / st.scale;
					has_updated = TRUE;
					break;
				case SDLK_k:
					st.scale /= 1.5;
					st.move_amount += st.move_amount / st.scale;
					has_updated = TRUE;
					break;
				}
				break;
			default:
				/* puts("Unknown event received"); */
				break;
			}
		}

		if (has_updated) {
			draw_loading_identifier(renderer);
			draw(renderer, &st);
			has_updated = FALSE;
		}
	}
	SDL_Quit();
	return 0;
}

void draw_loading_identifier(SDL_Renderer* r)
{
	SDL_SetRenderDrawColor(r, 255, 128, 0, 255);
	SDL_Rect rect = { .x = 0, .y = 0, .w = WIDTH, .h = 20 };
	SDL_RenderFillRect(r, &rect);
	SDL_RenderPresent(r);
}

void draw(SDL_Renderer* r, const State const* st)
{
	for (int x = 0; x < WIDTH; x++) {
		for (int y = 0; y < HEIGHT; y++) {
			double scale_x = (REAL_SET_END - REAL_SET_START) / st->scale;
			double scale_y = (IMAGINARY_SET_END - IMAGINARY_SET_START) / st->scale;

			double c_x = (REAL_SET_START + st->camera_x) + (x * scale_x);
			double c_y = (IMAGINARY_SET_START + st->camera_y) + (y * scale_y);

			MandelbrotResult result = mandelbrot(c_x, c_y);
			if (result.is_in) {
				SDL_SetRenderDrawColor(r, 0, 0, 0, 255);
			} else {
				SDL_SetRenderDrawColor(r,
						((int) (round(result.iteration_count * 900.0) / 80.0)) % 255,
						0, 255, 255);
			}

			SDL_Rect rect = { .x = x, .y = y, .w = 5, .h = 5 };
			SDL_RenderFillRect(r, &rect);
		}
	}

	SDL_RenderPresent(r);
}

void die(const char* c)
{
	puts(c);
	exit(1);
}

MandelbrotResult mandelbrot(double c_x, double c_y)
{
	double z_x = 0.0;
	double z_y = 0.0;
	double abs_value = 0.0;

	int i = 0;
	while (i < MAX_ITERATION && abs_value <= 2) {
		double z_sq_x = pow(z_x, 2) - pow(z_y, 2);
		double z_sq_y = 2 * z_x * z_y;

		z_x = z_sq_x + c_x;
		z_y = z_sq_y + c_y;

		// FIXME: two-arg sqrt??? what the hell is that?
		abs_value = sqrt(pow(z_x, 2) + pow(z_y, 2));

		i++;
	}

	MandelbrotResult result = { .is_in = abs_value <= 2, .iteration_count = i };
	return result;
}
