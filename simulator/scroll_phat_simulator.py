import threading
import sys
import pickle
import tkinter as tk
import signal

ROWS = 7
COLUMNS = 17
LED_SIZE_PX = 50
LINE_WIDTH_PX = 5

WINDOW_HEIGHT_PX = LED_SIZE_PX * ROWS + LINE_WIDTH_PX * (ROWS - 1)
WINDOW_WIDTH_PX = LED_SIZE_PX * COLUMNS + LINE_WIDTH_PX * (COLUMNS - 1)

DRAW_TIMEOUT_MS = 100


class ScrollPhatSimulator:
    def set_pixels(self, vals):
        raise NotImplementedError()

    def set_brightness(self, brightness):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def running(self):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()


class TkPhatSimulator(ScrollPhatSimulator):
    def __init__(self):
        self.brightness = 70
        self.do_run = True
        self.pixels = [[0] * ROWS for i in range(COLUMNS)]

        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.root.bind('<Control-c>', lambda _: self.destroy())
        self.root.bind("<Unmap>", lambda _: self.destroy())
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)

        self.root.title('scroll pHAT HD simulator')
        self.root.geometry('{}x{}'.format(WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX))
        self.canvas = tk.Canvas(
            self.root, width=WINDOW_WIDTH_PX, height=WINDOW_HEIGHT_PX)
        self.canvas.config(highlightthickness=0)

    def pixel_addr(self, x, y):
        """Translate an x,y coordinate to a pixel index."""
        if x > 8:
            x = x - 8
            y = 6 - (y + 8)
        else:
            x = 8 - x

        return x * 16 + y

    def run(self):
        try:
            self.draw_pixels()
            self.root.mainloop()
        except Exception as e:
            print(e)
            self.destroy()

    def destroy(self):
        self.do_run = False

    def running(self):
        return self.do_run

    def draw_pixels(self):
        if not self.running():
            self.root.destroy()
            return

        self.canvas.delete(tk.ALL)
        self.canvas.create_rectangle(
            0, 0, WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX, width=0, fill='black')

        for col in range(COLUMNS):
            for row in range(ROWS):
                b = self.pixels[col][row]
                color = '#{:02x}{:02x}{:02x}'.format(b, b, b)
                x = (LED_SIZE_PX + LINE_WIDTH_PX) * col
                y = (LED_SIZE_PX + LINE_WIDTH_PX) * row
                self.canvas.create_rectangle(x, y, x + LED_SIZE_PX, y + LED_SIZE_PX, width=0, fill=color)

        self.canvas.pack()

        self.root.after(DRAW_TIMEOUT_MS, self.draw_pixels)

    def set_pixels(self, vals):
        for col in range(COLUMNS):
            for row in range(ROWS):
                addr = self.pixel_addr(col, ROWS - (row + 1))
                self.pixels[col][row] = vals[addr]


class ReadThread:
    def __init__(self, scroll_phat_simulator):
        self.scroll_phat_simulator = scroll_phat_simulator
        self.stdin_thread = threading.Thread(
            target=self._read_stdin, daemon=True)

    def start(self):
        self.stdin_thread.start()

    def join(self):
        self.stdin_thread.join()

    def _read_stdin(self):
        while self.scroll_phat_simulator.running():
            try:
                self._handle_update(pickle.load(sys.stdin.buffer))
            except EOFError:
                self.scroll_phat_simulator.destroy()
            except Exception as err:
                self.scroll_phat_simulator.destroy()
                raise err

    def _handle_update(self, buffer):
        self.scroll_phat_simulator.set_pixels(buffer)


def main():
    print('starting scroll pHAT simulator')

    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    phat = TkPhatSimulator()
    thread = ReadThread(phat)
    thread.start()
    phat.run()
    thread.join()


if __name__ == "__main__":
    main()
