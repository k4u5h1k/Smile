from threading import Timer

class RepeatingTimer:
    def __init__(self, interval, function, args, **kwargs):
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.running = False
        self.thread = Timer(self.interval, self.handle_function)

    def handle_function(self):
            self.function(self.args, *self.kwargs)
            self.thread = Timer(self.interval, self.handle_function)
            self.thread.start()

    def run(self):
        if not self.running:
            self.running = True
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.cancel()

    def dec(self):
        if self.running:
            self.args =- 1


if __name__ == "__main__":

    from time import sleep

    def printer(test_arg):
        print("lorem ipsum")

    alive = RepeatingTimer(2, printer, 34)
    alive.run()
    sleep(6.1)
    alive.stop()
