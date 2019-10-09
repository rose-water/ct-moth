import time

class Vspeed():

    def __init__(self, integer = False, position = 0, delay = 0.01):
        self.last_time = time.monotonic()
        self.cur_time = self.last_time
        self.delay = delay
        self.speed = 25
        self.position = position
        self.last_position = position
        self.integer = integer
        self.seq_pos = 0
        self.seq_run = True
        self.seq_old = []
        self.loop_dir = 1
        self.RUNNING = True
        self.NOT_RUNNING = False
        self.CHANGED = True
        self.NO_CHANGE = False
        self.move(self.position)

    def move(self, value, speed = 50):
        changed = self.NO_CHANGE
        if value != self.position:
            self.cur_time = time.monotonic()
            diff_time = self.cur_time - self.last_time
            increment = speed / 10
            if diff_time > self.delay:
                # time to move
                if value > self.position:
                    self.position += increment
                    # are we there yet?
                    if value <= self.position:
                        self.position = value
                else:
                    self.position -= increment
                    # are we there yet?
                    if value >= self.position:
                        self.position = value
                self.last_time = time.monotonic()
                changed = self.CHANGED
            if self.integer:
                position = int(self.position)
                if position == self.last_position:
                    changed = self.NO_CHANGE
                    self.last_position = position
            else:
                position = self.position
            return position, self.RUNNING, changed
        else:
            # finished with move
            return self.position, self.NOT_RUNNING, changed

    def loop(self, low, lowspeed, high, highspeed):
        # loop from one position to another
        if high == self.position or low == self.position:
            # change directions
            self.loop_dir *= -1

        if self.loop_dir == 1:
            position, running, changed = self.move(high, highspeed)
        else:
            position, running, changed = self.move(low, lowspeed)
        return position, self.RUNNING, changed

    def sequence(self, sequence, loop = False):
        position = self.position
        seq_running = self.RUNNING
        changed = self.NO_CHANGE
        # perform a sequence of moves in this format [(90,10),(0,30),(180,50)]
        if sequence != self.seq_old:
            # reset with a new sequence
            self.seq_pos = 0
        # check for end of sequence
        if self.seq_pos < len(sequence):
            # are we paused?
            if self.seq_run:
                # move servo, if move is complete, go to the next position
                position, running, changed = self.move(sequence[self.seq_pos][0], sequence[self.seq_pos][1])
                if not running:
                    self.seq_pos +=1
                    # if looping, reset back the beginning of seq
                    if loop and self.seq_pos >= len(sequence):
                        self.seq_pos = 0
            else:
                seq_running = self.NOT_RUNNING
            self.seq_old = sequence
            return position, seq_running, changed
        else:
            # finished with sequence
            return position, self.NOT_RUNNING, self.NO_CHANGE

    def sequence_reset(self, position = 0):
        self.seq_pos = position

    def sequence_run(self, value = True):
        self.seq_run = value
